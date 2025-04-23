#!/bin/bash

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the modern UI
echo "Starting SuperNova AI with modern UI..."
streamlit run modern_ui.py
