@echo off
echo 🌱 CommuniFarm ESPHome Device Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import yaml" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo 🚀 Starting setup generator...
echo.

REM Run the setup generator
python setup_generator.py

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Copy secrets.yaml to secrets_local.yaml
echo 2. Edit secrets_local.yaml with your WiFi credentials
echo 3. Generate an API encryption key
echo 4. Flash the device with ESPHome
echo.
pause
