#!/bin/bash

# Install Playwright browsers
echo "Installing Playwright browsers..."
python -m playwright install --with-deps chromium

# Create necessary directories
mkdir -p /tmp/supernova_sandbox

# Set permissions
chmod -R 777 /tmp/supernova_sandbox

# Run Ollama setup script
echo "Setting up Ollama..."
./setup_ollama.sh

echo "Setup completed successfully!"
