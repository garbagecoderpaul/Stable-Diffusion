import sqlite3

# Database configuration with the SQLite database file name.
db_config = {
    'database': 'nft.db',
}

def create_database_tables(connection):
    cursor = connection.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS image")
    cursor.execute("DROP TABLE IF EXISTS character")
    cursor.execute("DROP TABLE IF EXISTS category")

    # Create the 'character' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS character (
        character_id INTEGER PRIMARY KEY,
        character_notion_id INTEGER UNIQUE,
        surname TEXT,
        faction TEXT,
        gender TEXT,
        property TEXT,
        position TEXT,
        historical TEXT,
        name TEXT,
        description_short TEXT,
        description_full TEXT
    )
    """)

    # Create the 'category' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        json_name TEXT
    )
    """)

    # Create the 'image' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image (
        image_id INTEGER PRIMARY KEY,
        img BLOB,
        img_hosting_link TEXT,
        ipfs_link TEXT,
        image_name TEXT,
        old_meta_json TEXT,
        unique_id TEXT,
        character_notion_id INTEGER,
        surname TEXT,
        json_name TEXT,
        category TEXT,
        json_version INTEGER,
        category_id INTEGER,
        character_id INTEGER,  -- Add this line to create the character_id column
        FOREIGN KEY (category_id) REFERENCES category (category_id),
        FOREIGN KEY (character_id) REFERENCES character (character_id)
    )
    """)

    connection.commit()

# Connect to the SQLite database
print("Connecting to the SQLite database...")
connection = sqlite3.connect('nft.db')

create_database_tables(connection)
connection.close()
print("Database nft.db tables created with relationships.")
