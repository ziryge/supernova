#!/usr/bin/env python3
"""
SuperNova AI Server

This script runs SuperNova AI as a server that can be accessed by others over the internet.
It includes additional security and logging features.
"""

import os
import sys
import logging
import socket
import argparse
import subprocess
import webbrowser
from datetime import datetime
import streamlit.web.bootstrap
from dotenv import load_dotenv

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"supernova_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a socket to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        logging.warning(f"Could not determine local IP: {e}")
        return "127.0.0.1"

def check_port_availability(port):
    """Check if the specified port is available."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port))
        s.close()
        return True
    except socket.error:
        return False

def find_available_port(start_port=8501, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if check_port_availability(port):
            return port
    logging.error(f"Could not find an available port after {max_attempts} attempts")
    return start_port  # Return the start port anyway, let Streamlit handle the error

def run_server(port=8501, open_browser=False, allow_remote=True):
    """Run the SuperNova AI server."""
    # Load environment variables
    load_dotenv()
    
    # Get local IP address
    local_ip = get_local_ip()
    
    # Check if port is available, find another if not
    if not check_port_availability(port):
        logging.warning(f"Port {port} is not available. Finding another port...")
        port = find_available_port(port)
    
    # Set Streamlit configuration
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    
    if allow_remote:
        os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
        os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
        os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
    
    # Print server information
    logging.info("=" * 60)
    logging.info("Starting SuperNova AI Server")
    logging.info("=" * 60)
    logging.info(f"Local access: http://localhost:{port}")
    
    if allow_remote:
        logging.info(f"Network access: http://{local_ip}:{port}")
        logging.info("")
        logging.info("To allow external access from the internet:")
        logging.info(f"1. Set up port forwarding on your router for port {port}")
        logging.info(f"2. Share your public IP address or domain name with others")
    
    logging.info("=" * 60)
    
    # Open browser if requested
    if open_browser:
        webbrowser.open(f"http://localhost:{port}")
    
    # Run the Streamlit app
    streamlit.web.bootstrap.run("agent_ui.py", "", [], [])

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SuperNova AI Server")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the server on")
    parser.add_argument("--no-browser", action="store_true", help="Don't open the browser automatically")
    parser.add_argument("--local-only", action="store_true", help="Only allow local connections")
    args = parser.parse_args()
    
    try:
        run_server(
            port=args.port,
            open_browser=not args.no_browser,
            allow_remote=not args.local_only
        )
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
