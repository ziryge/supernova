# SuperNova AI Server Setup Guide

This guide will help you set up SuperNova AI as a server that can be accessed by other people on your network or over the internet.

## Local Network Setup

To make SuperNova AI accessible to other devices on your local network:

1. Run the provided startup script:
   ```bash
   ./start_server.sh
   ```

2. The script will display the local network URL (e.g., `http://192.168.1.100:8501`).

3. Other devices on the same network can access SuperNova AI by entering this URL in their web browser.

## Internet Access Setup

To make SuperNova AI accessible from the internet:

1. **Set up port forwarding on your router**:
   - Log in to your router's admin panel (typically at `192.168.1.1` or `192.168.0.1`)
   - Find the port forwarding section (may be under "Advanced Settings", "NAT", or "Virtual Server")
   - Create a new port forwarding rule:
     - External port: 8501
     - Internal port: 8501
     - Internal IP address: Your computer's local IP (shown when you run `start_server.sh`)
     - Protocol: TCP

2. **Find your public IP address**:
   - Visit [whatismyip.com](https://www.whatismyip.com/) or search "what is my IP" on Google
   - Your public IP will be displayed (e.g., `203.0.113.1`)

3. **Access SuperNova AI from the internet**:
   - Use `http://YOUR_PUBLIC_IP:8501` (replace YOUR_PUBLIC_IP with your actual public IP)
   - If you have a domain name pointing to your IP, you can use that instead

## Security Considerations

For security when exposing SuperNova AI to the internet:

1. **Enable authentication**:
   - Open `auth_config.py`
   - Set `ENABLE_AUTH = True`
   - Change the default username and password
   - Generate a new secret key (instructions in the file)

2. **Consider using HTTPS**:
   - For proper security, set up HTTPS using a reverse proxy like Nginx or Caddy
   - You can get free SSL certificates from Let's Encrypt

3. **Use a dynamic DNS service** if your public IP changes frequently:
   - Services like No-IP, DuckDNS, or Dynu provide free dynamic DNS
   - This gives you a consistent domain name that updates when your IP changes

## Troubleshooting

- **Can't access from local network**: Check your firewall settings to ensure port 8501 is allowed
- **Can't access from internet**: Verify port forwarding is set up correctly and your ISP doesn't block incoming connections
- **Server stops when you close terminal**: Use a tool like `screen`, `tmux`, or `nohup` to keep the server running

## Advanced Setup

For a more robust setup, consider:

1. **Creating a systemd service** for automatic startup
2. **Setting up a reverse proxy** with Nginx or Caddy
3. **Using Docker** to containerize the application

## Need Help?

If you encounter issues with the server setup, check:
- Router documentation for port forwarding instructions
- Your ISP's policies (some block incoming connections or require business plans)
- Firewall settings on your computer
