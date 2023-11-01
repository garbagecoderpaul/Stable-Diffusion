import torch
import cv2
import os
import threading
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # or set it to a larger limit than the default

# Constants
INPUT_FOLDER = r"/workspace/train_img/127_Kolomoyskyi/train"
OUTPUT_FOLDER = r"/workspace/cropped_img"
YOLO_DETECTED_FOLDER = r"/workspace/yolo_detected"
ASPECT_RATIOS = [(1024, 1024)]
SAVE_TO_YOLO_DETECTED_FOLDER = True  # Set this to False if you don't want to save to YOLO detected folder

# Thread-safe variables and lock
counter_lock = threading.Lock()
image_processed_counter = 0
write_lock = threading.Lock()
model_lock = threading.Lock()

def resize_bbox_to_dimensions(bbox, target_width, target_height, img_width, img_height):
    x1, y1, x2, y2 = bbox
    current_width = x2 - x1
    current_height = y2 - y1
    desired_aspect_ratio = target_width / target_height
    current_aspect_ratio = current_width / current_height
    
    if current_aspect_ratio < desired_aspect_ratio:
        new_width = desired_aspect_ratio * current_height
        x1 -= (new_width - current_width) / 2
        x2 += (new_width - current_width) / 2
    elif current_aspect_ratio > desired_aspect_ratio:
        new_height = current_width / desired_aspect_ratio
        y1 -= (new_height - current_height) / 2
        y2 += (new_height - current_height) / 2

    x1 = max(x1, 0)
    y1 = max(y1, 0)
    x2 = min(x2, img_width)
    y2 = min(y2, img_height)

    return [int(x1), int(y1), int(x2), int(y2)]

created_folders = set()

def process_files(filelist):
    global image_processed_counter
    with counter_lock:
        model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'yolov7-e6e.pt', force_reload=False, trust_repo=True)
    for filename in filelist:
        try:  # Start of the try block
            img_path = os.path.join(INPUT_FOLDER, filename)
            image = cv2.imread(img_path)
            if image is None:
                raise ValueError(f"Could not read image {filename}")
            img_width, img_height = image.shape[1], image.shape[0]

            with model_lock:
                results = model(img_path)
            detections = results.pandas().xyxy[0]

            person_detected = detections[detections['name'] == 'person']
            if not person_detected.empty:
                x1, y1, x2, y2 = person_detected.iloc[0][['xmin', 'ymin', 'xmax', 'ymax']].astype(int)

                for target_width, target_height in ASPECT_RATIOS:
                    new_x1, new_y1, new_x2, new_y2 = resize_bbox_to_dimensions([x1, y1, x2, y2], target_width, target_height, img_width, img_height)
                    new_x1, new_y1 = max(new_x1, 0), max(new_y1, 0)
                    new_x2, new_y2 = min(new_x2, img_width), min(new_y2, img_height)
                    cropped_img = image[new_y1:new_y2, new_x1:new_x2]

                    aspect_folder = os.path.join(OUTPUT_FOLDER, f"{target_width}x{target_height}")
                    with counter_lock:
                        if aspect_folder not in created_folders:
                            if not os.path.exists(aspect_folder):
                                os.makedirs(aspect_folder)
                            created_folders.add(aspect_folder)

                    save_path = os.path.join(aspect_folder, filename)
                    quality = 100
                    cv2.imwrite(save_path, cropped_img, [cv2.IMWRITE_JPEG_QUALITY, quality])

                if SAVE_TO_YOLO_DETECTED_FOLDER:
                    if not os.path.exists(YOLO_DETECTED_FOLDER):
                        os.makedirs(YOLO_DETECTED_FOLDER)
                    yolo_detected_img_path = os.path.join(YOLO_DETECTED_FOLDER, filename)
                    cv2.imwrite(yolo_detected_img_path, results.render()[0])
                    
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")
        finally:
            with counter_lock:
                image_processed_counter += 1
                print(f"Processed {image_processed_counter}/{len(all_files)} images. Remaining: {len(all_files) - image_processed_counter}")

def split_list(lst, n):
    avg = len(lst) // n
    remainder = len(lst) % n
    start = 0
    results = []
    for i in range(n):
        end = start + avg + (1 if i < remainder else 0)
        results.append(lst[start:end])
        start = end
    return results

print("reading all image files may take a while please wait...")
all_files = os.listdir(INPUT_FOLDER)
NUM_THREADS = 1
split_files = split_list(all_files, NUM_THREADS)
print("all files read")
threads = []

for sublist in split_files:
    thread = threading.Thread(target=process_files, args=(sublist,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Processing complete!")
