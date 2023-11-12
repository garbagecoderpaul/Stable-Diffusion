import os

root_directory = "/workspace/train_img"

def rename_and_create_train_folder(root):
    subfolders = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]
    for subfolder in subfolders:
        subfolder_path = os.path.join(root, subfolder)
        raw_folder_path = os.path.join(subfolder_path, "raw")
        train_folder_path = os.path.join(subfolder_path, "train")

        # Rename the folder to 'raw' if it exists
        if os.path.exists(raw_folder_path):
            try:
                os.rename(subfolder_path, raw_folder_path)
                print(f"Renamed '{subfolder}' to 'raw'")
            except Exception as e:
                print(f"Failed to rename '{subfolder}' to 'raw': {e}")

        # Create the 'train' folder if it doesn't exist
        if not os.path.exists(train_folder_path):
            try:
                os.makedirs(train_folder_path, exist_ok=True)
                print(f"Created 'train' folder: '{train_folder_path}'")
            except Exception as e:
                print(f"Failed to create 'train' folder in '{subfolder}': {e}")

        # Check if the 'raw' folder contains files
        if not os.listdir(raw_folder_path):
            print(f"'raw' folder is empty in '{subfolder}'")
        else:
            # Now you can call the 'cropper_v8.py' script with the new paths
            os.system(f'python cropper_v8.py "{raw_folder_path}" "{train_folder_path}"')

if os.path.exists(root_directory):
    rename_and_create_train_folder(root_directory)
else:
    print(f"Root directory {root_directory} does not exist.")
