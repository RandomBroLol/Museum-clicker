@echo off
echo Installing required libraries for Claxes pc...

REM Check if pip is installed
pip --version
IF %ERRORLEVEL% NEQ 0 (
    echo Pip not found. Please install Python and ensure pip is included in your PATH.
    exit /b 1
)

REM Install required libraries
pip install pillow
pip install watchdog

echo Required libraries installed successfully!
pause
