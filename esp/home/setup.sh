#!/bin/bash

echo "🌱 CommuniFarm ESPHome Device Setup"
echo "===================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    echo "Please install Python3 from your package manager"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import yaml" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

echo
echo "🚀 Starting setup generator..."
echo

# Run the setup generator
python3 setup_generator.py

echo
echo "✅ Setup complete!"
echo
echo "Next steps:"
echo "1. Copy secrets.yaml to secrets_local.yaml"
echo "2. Edit secrets_local.yaml with your WiFi credentials"
echo "3. Generate an API encryption key"
echo "4. Flash the device with ESPHome"
echo
