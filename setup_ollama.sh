#!/bin/bash
# Script to install and run Ollama on Streamlit Cloud

echo "Setting up Ollama for Streamlit Cloud..."

# Check if we're running on Streamlit Cloud
if [[ -z "${STREAMLIT_SHARING_MODE}" && -z "${STREAMLIT_RUNTIME}" ]]; then
    echo "Not running on Streamlit Cloud, skipping Ollama setup"
    exit 0
fi

# Create directories
mkdir -p /tmp/ollama
cd /tmp/ollama

# Download Ollama
echo "Downloading Ollama..."
curl -L https://ollama.com/download/ollama-linux-amd64 -o ollama
chmod +x ollama

# Start Ollama server in the background
echo "Starting Ollama server..."
./ollama serve &
sleep 5  # Wait for server to start

# Pull the required models
echo "Pulling Ollama models..."
./ollama pull llama3
./ollama pull mistral

echo "Ollama setup complete!"
