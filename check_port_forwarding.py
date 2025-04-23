#!/usr/bin/env python3
"""
Port Forwarding Checker for SuperNova AI

This script checks if your port forwarding is set up correctly
by attempting to connect to your public IP address.
"""

import os
import sys
import socket
import argparse
import requests
import time
from urllib.parse import urlparse

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Could not determine local IP: {e}")
        return "127.0.0.1"

def get_public_ip():
    """Get the public IP address of the machine."""
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        return response.text
    except Exception as e:
        print(f"Could not determine public IP: {e}")
        return None

def check_port(ip, port, timeout=5):
    """Check if a port is open on a given IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port: {e}")
        return False

def check_streamlit_server(url, timeout=5):
    """Check if a Streamlit server is running at the given URL."""
    try:
        response = requests.get(url, timeout=timeout)
        return "streamlit" in response.text.lower()
    except Exception:
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Port Forwarding Checker for SuperNova AI")
    parser.add_argument("--port", type=int, default=8501, help="Port to check (default: 8501)")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout in seconds (default: 5)")
    args = parser.parse_args()
    
    port = args.port
    timeout = args.timeout
    
    print("=" * 60)
    print("SuperNova AI Port Forwarding Checker")
    print("=" * 60)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"Local IP address: {local_ip}")
    
    # Check if local server is running
    print("\nChecking if SuperNova AI is running locally...")
    if check_port("localhost", port, timeout):
        print(f"✅ SuperNova AI is running on localhost:{port}")
        
        # Check if it's a Streamlit server
        if check_streamlit_server(f"http://localhost:{port}", timeout):
            print("✅ Confirmed Streamlit server is running")
        else:
            print("⚠️ Server is running but doesn't appear to be Streamlit")
    else:
        print(f"❌ SuperNova AI is not running on localhost:{port}")
        print(f"   Please start the server first with: python server.py")
        return
    
    # Get public IP
    print("\nChecking your public IP address...")
    public_ip = get_public_ip()
    if not public_ip:
        print("❌ Could not determine your public IP address")
        return
    
    print(f"Public IP address: {public_ip}")
    
    # Check if public IP is different from local IP
    if public_ip == local_ip:
        print("⚠️ Your public IP is the same as your local IP.")
        print("   This usually means you're on a business or university network")
        print("   and port forwarding may not be possible.")
        return
    
    # Check port forwarding
    print("\nChecking port forwarding...")
    print(f"Attempting to connect to {public_ip}:{port} from the internet...")
    print("This may take a few seconds...")
    
    # Use an external service to check if the port is open
    try:
        print("\nMethod 1: Using external service to check port...")
        response = requests.get(f"https://portchecker.io/api/v1/check/{public_ip}/{port}", timeout=10)
        data = response.json()
        if data.get("status") == "open":
            print(f"✅ Port {port} is open on your public IP")
        else:
            print(f"❌ Port {port} is not open on your public IP")
    except Exception as e:
        print(f"❌ Could not check port using external service: {e}")
    
    # Try to connect directly
    print("\nMethod 2: Trying direct connection...")
    if check_port(public_ip, port, timeout):
        print(f"✅ Successfully connected to {public_ip}:{port}")
        
        # Check if it's a Streamlit server
        if check_streamlit_server(f"http://{public_ip}:{port}", timeout):
            print("✅ Confirmed Streamlit server is accessible")
        else:
            print("⚠️ Server is accessible but doesn't appear to be Streamlit")
    else:
        print(f"❌ Could not connect to {public_ip}:{port}")
        print("   This could mean:")
        print("   1. Port forwarding is not set up correctly on your router")
        print("   2. Your ISP is blocking incoming connections")
        print("   3. A firewall is blocking the connection")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Local access: http://localhost:{port}")
    print(f"Network access: http://{local_ip}:{port}")
    print(f"Internet access: http://{public_ip}:{port}")
    print("\nIf you're having trouble with port forwarding:")
    print("1. Check your router's port forwarding settings")
    print("2. Make sure your firewall allows incoming connections on port 8501")
    print("3. Some ISPs block incoming connections - check with your provider")
    print("=" * 60)

if __name__ == "__main__":
    main()
