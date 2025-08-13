#!/bin/bash

echo "Building Augment VIP GUI Executable..."
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Build executable
echo "Building executable with PyInstaller..."
pyinstaller --clean augment_vip.spec

if [ $? -eq 0 ]; then
    echo
    echo "================================"
    echo "Build completed successfully!"
    echo "Executable location: dist/AugmentVIP"
    echo "================================"
    echo
    
    # Ask if user wants to run the executable
    read -p "Do you want to run the executable now? (y/n): " run_exe
    if [[ "$run_exe" =~ ^[Yy]$ ]]; then
        echo "Running executable..."
        ./dist/AugmentVIP
    fi
else
    echo
    echo "================================"
    echo "Build failed! Check the error messages above."
    echo "================================"
fi
