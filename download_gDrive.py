import re
import os

# Prompt the user for FILELINK and FILENAME
filelink = input("Enter the Google Drive File LINK: ")
filename = input("Enter the FILENAME (e.g. 777shevchenko): ")

# Input string with placeholders
input_string = "wget --load-cookies /tmp/cookies.txt \"https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\\1\\n/p')&id=FILEID\" -O FILENAME && rm -rf /tmp/cookies.txt"

def extract_fileid(input_string):
    # Define a regular expression pattern to match the desired part
    pattern = r"/d/([^/]+)/"

    # Use re.search to find the match in the input string
    match = re.search(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the desired part (group 1)
        fileid = match.group(1)
        return fileid
    else:
        return None
        print("FILEID not found.")

def substitute_parameters(input_string, fileid, filename):
    # Use regular expressions to find and substitute FILEID and FILENAME
    input_string = re.sub(r'FILEID', fileid, input_string)
    input_string = re.sub(r'FILENAME', filename, input_string)

    return input_string

def concat_extention(input_string):
    # Concatenate the input string with ".safetensors" extention
    result = input_string + ".safetensors"
    return result

# Concatenate the file extention
fullname = concat_extention(filename)
print("Concatenated result:", fullname)

# Perform fileid extraction
fileid = extract_fileid(filelink)

# Perform parameter substitution
result = substitute_parameters(input_string, fileid, fullname)

# Print the modified string
print("Modified string:")
print(result)

# Run the command
os.system(result)
