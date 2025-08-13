@echo off
echo 🚀 ONE-CLICK BUILD - Augment VIP Multi-Platform
echo ===============================================
echo Building executable for all platforms from one script!
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo 🧹 Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "releases" rmdir /s /q "releases"

echo 📦 Installing/updating dependencies...
pip install --upgrade pip
pip install --upgrade pyinstaller>=5.0 PySide6>=6.0 psutil click

echo 🏗️ Building executable for your platform...
pyinstaller --clean --noconfirm ^
    --onefile ^
    --windowed ^
    --name AugmentVIP ^
    --add-data "src;src" ^
    --add-data "requirements.txt;." ^
    --hidden-import PySide6.QtCore ^
    --hidden-import PySide6.QtGui ^
    --hidden-import PySide6.QtWidgets ^
    --hidden-import psutil ^
    --hidden-import click ^
    main.py

if %ERRORLEVEL% == 0 (
    echo.
    echo 🎉 BUILD SUCCESS! 
    echo ================
    echo ✅ Executable created: dist\AugmentVIP.exe
    echo ✅ Ready to distribute on Windows
    echo ✅ Self-contained - no dependencies needed
    echo.
    echo � USAGE:
    echo   • Run GUI: python main.py
    echo   • Run CLI: python cli.py  
    echo   • Run EXE: dist\AugmentVIP.exe
    echo.
    
    REM Create simple release structure
    if not exist "releases" mkdir "releases"
    copy "dist\AugmentVIP.exe" "releases\"
    
    echo 📦 Release ready in: releases\AugmentVIP.exe
    echo.
    
    REM Ask to run
    set /p run_exe="🎯 Run the executable now? (y/n): "
    if /i "%run_exe%"=="y" (
        echo Starting AugmentVIP...
        start dist\AugmentVIP.exe
    )
) else (
    echo.
    echo ❌ BUILD FAILED! Check errors above.
    echo You can still run: python main.py
)

echo.
pause
