#!/bin/bash

# Create a virtual environment folder
echo "Creating venv"
if [ ! -d "venv" ]; then
    python3 -m venv venv
else
    echo "venv folder already exists, skipping creating a new venv..."
fi

# Activate the virtual environment
source venv/bin/activate

echo "Installing requirements"
# Install packages from requirements.txt
pip install -r requirements.txt

# Show completion message
echo "Virtual environment created and requirements installed properly"

# Pause to keep the terminal open (optional)
read -p "Press Enter to continue..."

# Deactivate the virtual environment
deactivate
