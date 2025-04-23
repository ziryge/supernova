# Hosting SuperNova AI on Your PC

This guide will help you set up SuperNova AI as a server on your PC that others can access through your site without them needing to do anything.

## Prerequisites

- A computer that can stay on while you want the service to be available
- A home internet connection with a public IP address
- Administrative access to your router for port forwarding
- Optional: A domain name (for easier access)

## Step 1: Set Up SuperNova AI Server

### Windows

1. **Install Required Dependencies**
   ```bash
   pip install pywin32
   ```

2. **Run as a Windows Service (starts automatically with Windows)**
   ```bash
   # Install the service (run as Administrator)
   python windows_service.py install
   
   # Start the service
   python windows_service.py start
   ```

3. **Or Run Manually (doesn't start automatically)**
   ```bash
   python server.py
   ```

### Linux

1. **Set Up as a Systemd Service (starts automatically)**
   ```bash
   # Edit the service file with your username and path
   nano supernova-ai.service
   
   # Copy to systemd directory
   sudo cp supernova-ai.service /etc/systemd/system/
   
   # Reload systemd
   sudo systemctl daemon-reload
   
   # Enable and start the service
   sudo systemctl enable supernova-ai.service
   sudo systemctl start supernova-ai.service
   ```

2. **Or Run Manually (doesn't start automatically)**
   ```bash
   python3 server.py
   ```

### macOS

1. **Create a Launch Agent (starts automatically)**
   ```bash
   # Create the launch agent directory if it doesn't exist
   mkdir -p ~/Library/LaunchAgents
   
   # Copy the provided plist file
   cp com.supernova.ai.plist ~/Library/LaunchAgents/
   
   # Edit the file to set your username and path
   nano ~/Library/LaunchAgents/com.supernova.ai.plist
   
   # Load the launch agent
   launchctl load ~/Library/LaunchAgents/com.supernova.ai.plist
   ```

2. **Or Run Manually (doesn't start automatically)**
   ```bash
   python3 server.py
   ```

## Step 2: Set Up Port Forwarding on Your Router

1. **Find Your Local IP Address**
   - Windows: Open Command Prompt and type `ipconfig`
   - Linux/macOS: Open Terminal and type `ifconfig` or `ip addr`
   - Look for your IPv4 address (usually starts with 192.168.x.x or 10.0.x.x)

2. **Access Your Router's Admin Panel**
   - Open a web browser and enter your router's IP address (usually 192.168.0.1 or 192.168.1.1)
   - Log in with your router's admin credentials

3. **Set Up Port Forwarding**
   - Find the "Port Forwarding" section (might be under "Advanced Settings", "NAT", or "Virtual Server")
   - Create a new port forwarding rule:
     - External port: 8501 (or your chosen port)
     - Internal port: 8501 (or your chosen port)
     - Internal IP address: Your computer's local IP address
     - Protocol: TCP
     - Name: SuperNovaAI

4. **Test Your Port Forwarding**
   - Visit [https://www.yougetsignal.com/tools/open-ports/](https://www.yougetsignal.com/tools/open-ports/)
   - Enter your port (8501) and check if it's open

## Step 3: Set Up a Domain Name (Optional but Recommended)

### Option 1: Use a Dynamic DNS Service (Free)

1. **Sign up for a free Dynamic DNS service**
   - [No-IP](https://www.noip.com/)
   - [DuckDNS](https://www.duckdns.org/)
   - [Dynu](https://www.dynu.com/)

2. **Install the Dynamic DNS client** on your computer to keep your IP address updated

3. **Configure your domain** to point to your public IP address

### Option 2: Use Your Own Domain Name

1. **Purchase a domain name** from a registrar like Namecheap, GoDaddy, or Google Domains

2. **Set up an A record** pointing to your public IP address

3. **Use a Dynamic DNS updater** to keep your domain pointing to your IP address if it changes

## Step 4: Access Your SuperNova AI Server

### From Your Local Network

- Open a web browser and go to `http://localhost:8501` or `http://your_local_ip:8501`

### From the Internet

- Without a domain: `http://your_public_ip:8501`
- With a domain: `http://your_domain.com:8501`

## Step 5: Security Considerations

1. **Enable Authentication**
   - Edit `auth_config.py`
   - Set `ENABLE_AUTH = True`
   - Update the username and password

2. **Set Up HTTPS (Optional but Recommended)**
   - Install a reverse proxy like Nginx or Caddy
   - Obtain a free SSL certificate from Let's Encrypt
   - Configure the reverse proxy to handle HTTPS

3. **Firewall Configuration**
   - Make sure your firewall allows traffic on port 8501
   - Consider restricting access to specific IP addresses if needed

## Troubleshooting

### Server Won't Start

- Check the logs in the `logs` directory
- Make sure all dependencies are installed
- Verify that port 8501 is not already in use

### Can't Access from Local Network

- Check if the server is running (`http://localhost:8501`)
- Verify your firewall settings
- Make sure you're using the correct local IP address

### Can't Access from Internet

- Verify port forwarding is set up correctly
- Check if your ISP blocks incoming connections
- Make sure your public IP hasn't changed
- Try accessing with your public IP instead of domain name

### Domain Name Not Working

- Verify your DNS settings
- Make sure your dynamic DNS updater is running
- Check if your public IP has changed

## Maintenance

1. **Keep SuperNova AI Updated**
   ```bash
   git pull
   pip install -r requirements.txt
   ```

2. **Monitor Logs**
   - Check the logs in the `logs` directory regularly

3. **Backup Your Data**
   - Regularly backup your SuperNova AI directory

## Need More Help?

- Check the SuperNova AI documentation
- Search for router-specific port forwarding instructions
- Contact your ISP if you're having trouble with port forwarding
