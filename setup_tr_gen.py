import os
import json
import csv

while True:
    # Step 1: Check if "Book2_name.csv" exists in the directory
    csv_file_path = '/workspace/Stable-Diffusion/Book2_name.csv'
    if os.path.isfile(csv_file_path):
        # File exists, read it and count the number of rows
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            row_count = sum(1 for row in csv_reader)
            print(f"Number of rows in 'Book2_name.csv': {row_count}")
        break
    else:
        # File doesn't exist, ask the user to upload it
        print("Please upload 'Book2_name.csv' to the directory '/workspace/Stable-Diffusion' and press Enter when done.")
        input("Press Enter to continue...")

# Step 2: Create an empty dictionary
data_dict = {}

# Step 3: Ask for gender
gender = input("Enter gender ('m' for male, 'f' for female): ").strip().lower()
if gender in ['m', 'f']:
    data_dict['gender'] = gender
else:
    print("Invalid input. Please enter 'm' for male or 'f' for female.")

# Step 4: Ask for faction
factions = {
    'r': 'rus.csv',
    'u': 'ukr.csv',
    'n': 'ntr.csv',
    'g': 'good_rus.csv',
    'c': 'cor_ukr.csv',
}
faction = input('''Enter faction \n 'r': 'rus.csv' \n 'u': 'ukr.csv' \n 'n': 'ntr.csv' \n 'g': 'good_rus.csv' \n 'c': 'cor_ukr.csv' ''').strip().lower()
if faction in factions:
    data_dict['faction'] = faction
else:
    print("Invalid faction. Please enter one of the valid codes: 'r', 'u', 'n', 'g', 'c'.")

# Step 5: Write the dictionary to "prompt_log.json"
with open('/workspace/Stable-Diffusion/prompt_log.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print("Data saved to 'prompt_log.json'.")
