import os

root_directory = "/workspace/train_img"

def rename_and_create_train_folder(root):
    subfolders = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]
    for subfolder in subfolders:
        subfolder_path = os.path.join(root, subfolder)
        raw_folder_path = os.path.join(subfolder_path, "raw")
        train_folder_path = os.path.join(subfolder_path, "train")

        # Check if "raw" and "train" folders already exist
        if not os.path.exists(raw_folder_path) or not os.path.exists(train_folder_path):
            try:
                if not os.path.exists(raw_folder_path):
                    os.rename(subfolder_path, raw_folder_path)
                    print(f"Renamed {subfolder_path} to {raw_folder_path}")
                else:
                    print(f"'raw' folder already exists in {subfolder_path}")

                # Create the 'train' folder if it doesn't exist
                if not os.path.exists(train_folder_path):
                    os.makedirs(train_folder_path, exist_ok=True)
                    print(f"Created 'train' folder: {train_folder_path}")

                else:
                    print(f"'train' folder already exists in {subfolder_path}")
            except Exception as e:
                print(f"Failed to rename or create folders in {subfolder_path}: {e}")

            # Now you can call the 'cropper_v7.py' script with the new paths
            os.system(f'python cropper_v8.py "{raw_folder_path}" "{train_folder_path}"')
if os.path.exists(root_directory):
    rename_and_create_train_folder(root_directory)
else:
    print(f"Root directory {root_directory} does not exist.")
