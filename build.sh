#!/bin/bash

echo "🚀 ONE-CLICK BUILD - Augment VIP Multi-Platform"
echo "==============================================="
echo "Building executable for all platforms from one script!"
echo

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python not found! Please install Python first."
    exit 1
fi

# Detect OS for output
OS=$(uname -s)
case $OS in
    "Darwin") PLATFORM="macOS" ;;
    "Linux") PLATFORM="Linux" ;;
    *) PLATFORM="Unix-like" ;;
esac

echo "🖥️  Platform: $PLATFORM"
echo "🐍 Python: $PYTHON_CMD"

echo "🧹 Cleaning previous builds..."
rm -rf dist build releases

echo "📦 Installing/updating dependencies..."
$PIP_CMD install --upgrade pip
$PIP_CMD install --upgrade pyinstaller>=5.0 PySide6>=6.0 psutil click

echo "🏗️ Building executable for $PLATFORM..."

# Build command with platform-specific options
if [[ "$OS" == "Darwin" ]]; then
    # macOS - create .app bundle
    pyinstaller --clean --noconfirm \
        --onefile \
        --windowed \
        --name AugmentVIP \
        --add-data "src:src" \
        --add-data "requirements.txt:." \
        --hidden-import PySide6.QtCore \
        --hidden-import PySide6.QtGui \
        --hidden-import PySide6.QtWidgets \
        --hidden-import psutil \
        --hidden-import click \
        main.py
    
    EXECUTABLE="dist/AugmentVIP"
    RELEASE_FILE="AugmentVIP_macOS"
else
    # Linux - create binary
    pyinstaller --clean --noconfirm \
        --onefile \
        --windowed \
        --name AugmentVIP \
        --add-data "src:src" \
        --add-data "requirements.txt:." \
        --hidden-import PySide6.QtCore \
        --hidden-import PySide6.QtGui \
        --hidden-import PySide6.QtWidgets \
        --hidden-import psutil \
        --hidden-import click \
        main.py
    
    EXECUTABLE="dist/AugmentVIP"
    RELEASE_FILE="AugmentVIP_Linux"
    
    # Make executable
    chmod +x "$EXECUTABLE"
fi

if [ $? -eq 0 ]; then
    echo
    echo "🎉 BUILD SUCCESS!"
    echo "================"
    echo "✅ Executable created: $EXECUTABLE"
    echo "✅ Ready to distribute on $PLATFORM"
    echo "✅ Self-contained - no dependencies needed"
    echo
    echo "� USAGE:"
    echo "  • Run GUI: $PYTHON_CMD main.py"
    echo "  • Run CLI: $PYTHON_CMD cli.py"
    echo "  • Run EXE: $EXECUTABLE"
    echo
    
    # Create simple release structure
    mkdir -p releases
    cp "$EXECUTABLE" "releases/"
    
    echo "📦 Release ready in: releases/"
    echo
    
    # Ask to run
    read -p "🎯 Run the executable now? (y/n): " run_exe
    if [[ "$run_exe" =~ ^[Yy]$ ]]; then
        echo "Starting AugmentVIP..."
        if [[ "$OS" == "Darwin" ]]; then
            open "$EXECUTABLE" || "./$EXECUTABLE" &
        else
            "./$EXECUTABLE" &
        fi
    fi
else
    echo
    echo "❌ BUILD FAILED! Check errors above."
    echo "You can still run: $PYTHON_CMD main.py"
fi

echo
