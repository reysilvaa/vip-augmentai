@echo off
echo Building Augment VIP GUI Executable...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Build executable
echo Building executable with PyInstaller...
pyinstaller --clean augment_vip.spec

if %ERRORLEVEL% == 0 (
    echo.
    echo ================================
    echo Build completed successfully!
    echo Executable location: dist\AugmentVIP.exe
    echo ================================
    echo.
    
    REM Ask if user wants to run the executable
    set /p run_exe="Do you want to run the executable now? (y/n): "
    if /i "%run_exe%"=="y" (
        echo Running executable...
        start dist\AugmentVIP.exe
    )
) else (
    echo.
    echo ================================
    echo Build failed! Check the error messages above.
    echo ================================
)

pause
