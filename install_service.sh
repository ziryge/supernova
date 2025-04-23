#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Get the current username
CURRENT_USER=$(whoami)

# Update the service file with the correct username and path
sed -i "s|User=YOUR_USERNAME|User=$CURRENT_USER|g" "$SCRIPT_DIR/supernova-ai.service"
sed -i "s|WorkingDirectory=/path/to/supernova-ai|WorkingDirectory=$SCRIPT_DIR|g" "$SCRIPT_DIR/supernova-ai.service"

echo "========================================================"
echo "SuperNova AI Service Installation"
echo "========================================================"
echo "This script will install SuperNova AI as a systemd service"
echo "so it starts automatically when your computer boots."
echo ""
echo "You will need sudo privileges to install the service."
echo "========================================================"
echo ""

# Ask for confirmation
read -p "Do you want to continue? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation cancelled."
    exit 1
fi

# Copy the service file to the systemd directory
echo "Copying service file to systemd directory..."
sudo cp "$SCRIPT_DIR/supernova-ai.service" /etc/systemd/system/

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service
echo "Enabling SuperNova AI service..."
sudo systemctl enable supernova-ai.service

# Start the service
echo "Starting SuperNova AI service..."
sudo systemctl start supernova-ai.service

# Check the status
echo "Checking service status..."
sudo systemctl status supernova-ai.service

echo ""
echo "========================================================"
echo "Installation complete!"
echo "========================================================"
echo "SuperNova AI will now start automatically when your computer boots."
echo ""
echo "To manually control the service, use these commands:"
echo "  - Start: sudo systemctl start supernova-ai.service"
echo "  - Stop: sudo systemctl stop supernova-ai.service"
echo "  - Restart: sudo systemctl restart supernova-ai.service"
echo "  - Status: sudo systemctl status supernova-ai.service"
echo "========================================================"
