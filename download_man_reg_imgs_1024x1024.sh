apt update

# Define the target directory
target_dir="/workspace/regimages"

# Create the target directory if it doesn't exist
mkdir -p "$target_dir"

# List of zip file URLs
zip_urls=(
    #"https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/raw_2735_imgs.zip"

	"https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/1024x1024_2734_imgs.zip"
)

# Install p7zip-full package
yes | apt-get install p7zip-full

# Loop through the zip URLs and download/extract
for url in "${zip_urls[@]}"; do
    # Get the filename from the URL
    file_name=$(basename "$url")

    # Download the zip file
    wget "$url" -P "$target_dir"

    # Extract the zip file with password
    7z x -psecourses "$target_dir/$file_name" -o"$target_dir"

    # Remove the downloaded zip file
    rm "$target_dir/$file_name"
done

echo "All zip files downloaded and extracted."
