import os

root_directory = "/workspace/train_img"

def rename_target_folders(root):
    subfolders = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]
    for subfolder in subfolders:
        subfolder_path = os.path.join(root, subfolder)
        target_folders = [f for f in os.listdir(subfolder_path) if os.path.isdir(os.path.join(subfolder_path, f))]
        for target_folder in target_folders:
            if target_folder != "train":
                target_folder_path = os.path.join(subfolder_path, target_folder)
                try:
                    os.rename(target_folder_path, os.path.join(subfolder_path, "train"))
                    print(f"Renamed {target_folder_path} to {os.path.join(subfolder_path, 'train')}")
                except Exception as e:
                    print(f"Failed to rename {target_folder_path}: {e}")

if os.path.exists(root_directory):
    rename_target_folders(root_directory)
else:
    print(f"Root directory {root_directory} does not exist.")
