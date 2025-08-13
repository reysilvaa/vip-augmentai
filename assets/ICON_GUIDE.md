 Icon Setup Guide

## Option 1: Use existing .ico file
1. Copy your .ico file to: assets/app_icon.ico
2. Update PyInstaller spec file (see below)

## Option 2: Create icon from image
1. Convert PNG/JPG to ICO using online tools like:
   - https://convertio.co/png-ico/
   - https://favicon.io/favicon-converter/
2. Save as: assets/app_icon.ico

## Option 3: Generate programmatically (advanced)
Run the create_icon.py script in this directory.

## Recommended Icon Sizes for ICO:
- 16x16, 32x32, 48x48, 64x64, 128x128, 256x256

## After creating icon, update these files:
1. augment_vip.spec (line with icon=None)
2. main_window.py (setWindowIcon)
3. Rebuild with build_gui.bat
