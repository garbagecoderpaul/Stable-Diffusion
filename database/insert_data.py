import os
import re
import sqlite3
import csv
import json

#====================1. Functions and Variables configuration
base_img_folder = '/workspace/images'
nft_db = 'nft.db'

# Connect to the SQLite database
connection = sqlite3.connect(nft_db)
cursor = connection.cursor()

def insert_data_from_csv(file_path, table_name, field_names):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute(f"""
            INSERT OR IGNORE INTO {table_name} ({', '.join(field_names)})
            VALUES ({', '.join(['?'] * len(field_names))})
            """, tuple(row[field] for field in field_names))

# Function to parse image_name using regular expressions
def parse_image_name(image_name):
    match = re.match(r'(?P<unique_id>[\da-fA-F-]+)_(?P<character_notion_id>\d+)_(?P<surname>[^_]+)_(?P<json_name>[\w]+)(?P<version>\d+)', image_name)

    if match:
        return (
            match.group('unique_id'),
            match.group('character_notion_id'),
            match.group('surname'),
            match.group('json_name'),
            match.group('version')
        )
    else:
        return None, None, None, None, None

# Mapping between json_name and name
json_name_mapping = {
    'demon': 'demon',
    'zombie': 'zombie',
    'clown': 'clown',
    'vamp': 'vampire',
    'mil_rus': 'military',
    'mil_ukr': 'military',
    'pirate': 'pirate',
    'primordial': 'primordial',
    'angel': 'angel',
    'cowboy': 'cowboy',
    'wizard': 'wizard',
    'warrior': 'warrior',
    'jedi': 'jedi',
    'science_robo': 'scientist',
    'science_bio': 'scientist',
    'anthtop_bird': 'anthropomorth',
    'surreal': 'surrealism',
    'cubism': 'cubism',
    'impressionism': 'impressionism',
    'psychedelic': 'psychedelic',
    'cyborg': 'cyborg',
    'slums': 'slums',
    'cryptopunk': 'cryptopunk',
    'nuclear': 'radioactive'
}

#====================2. Character and Category CSVs
# Character: insert from character.csv
insert_data_from_csv('character.csv', 'character', [
    'character_notion_id', 'surname', 'faction', 'gender', 'property',
    'position', 'historical', 'name', 'description_short', 'description_full'
])

# Category: insert from category.csv
insert_data_from_csv('category.csv', 'category', ['name', 'json_name'])

#====================3. Images and Metadata

# Iterate through all folders in the base image folder
for folder_name in os.listdir(base_img_folder):
    img_folder = os.path.join(base_img_folder, folder_name)

    # Check if there are any files in the folder
    if not any(filename.endswith('.png') for filename in os.listdir(img_folder)):
        print(f"No image files found in folder: {folder_name}. Skipping...")
        continue

    # Iterate through downloaded files in the current folder and insert data into the 'image' table
    count = 0
    for root, dirs, files in os.walk(img_folder):
        for filename in files:
            if filename.endswith('.png'):
                img_path = os.path.join(root, filename)
                with open(img_path, 'rb') as img_file:
                    img_data = img_file.read()
                
                image_name = os.path.splitext(filename)[0]
                
                # Use the parse_image_name function
                (
                    unique_id,
                    character_notion_id,
                    surname,
                    json_name,
                    json_version
                ) = parse_image_name(image_name)
                
                # Map json_name to name
                category = json_name_mapping.get(json_name, json_name)

                if unique_id is not None:
                    meta_json_path = os.path.join(root, f'{image_name}.png.json')
                    
                    # Check if the meta_json_path exists
                    if not os.path.exists(meta_json_path):
                        print(f"Metadata file not found: {meta_json_path}. Skipping...")
                        continue

                    with open(meta_json_path, 'r') as json_file:
                        json_content = json.load(json_file)

                    # Insert data into the 'image' table
                    cursor.execute("""
                    INSERT INTO image (img, image_name, old_meta_json, unique_id, character_notion_id, surname, json_name, json_version, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (img_data, image_name, json.dumps(json_content), unique_id, character_notion_id, surname, json_name, json_version, category))

                    count += 1

    # Establish relations between image, category, and character tables
    cursor.execute("""
    UPDATE image
    SET category_id = category.category_id,
        character_id = character.character_id
    FROM category, character
    WHERE image.category = category.name
    AND image.character_notion_id = character.character_notion_id
    """)

    connection.commit()
    print(f"DB writing finished. {count} images added to the DB for folder {folder_name}")

# Close the database connection
connection.close()
