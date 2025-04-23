#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Get the local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')

# Display server information
echo "========================================================"
echo "Starting SuperNova AI Server"
echo "========================================================"
echo "Local Network Access: http://$LOCAL_IP:8501"
echo "Local Access: http://localhost:8501"
echo ""
echo "To allow external access, make sure port 8501 is forwarded"
echo "in your router settings to this computer ($LOCAL_IP)"
echo "========================================================"

# Start the Streamlit server
streamlit run agent_ui.py
