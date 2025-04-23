"""
Windows Service for SuperNova AI

This script allows SuperNova AI to run as a Windows service that starts automatically
when your computer boots up.

Installation:
1. Install the required package: pip install pywin32
2. Run this script with admin privileges: python windows_service.py install
3. Start the service: python windows_service.py start

Removal:
1. Stop the service: python windows_service.py stop
2. Remove the service: python windows_service.py remove
"""

import os
import sys
import time
import logging
import subprocess
import win32serviceutil
import win32service
import win32event
import servicemanager

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "supernova_service.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

class SuperNovaAIService(win32serviceutil.ServiceFramework):
    """Windows Service for SuperNova AI."""
    
    _svc_name_ = "SuperNovaAI"
    _svc_display_name_ = "SuperNova AI Server"
    _svc_description_ = "Runs SuperNova AI as a server that can be accessed by others over the internet."
    
    def __init__(self, args):
        """Initialize the service."""
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None
        
    def SvcStop(self):
        """Stop the service."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        
        # Terminate the process if it's running
        if self.process:
            try:
                self.process.terminate()
                logging.info("SuperNova AI server process terminated")
            except Exception as e:
                logging.error(f"Error terminating process: {e}")
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        
    def SvcDoRun(self):
        """Run the service."""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        self.main()
        
    def main(self):
        """Main service function."""
        logging.info("Starting SuperNova AI service")
        
        # Get the path to the server script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_script = os.path.join(script_dir, "server.py")
        python_exe = sys.executable
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        # Start the server process
        try:
            self.process = subprocess.Popen(
                [python_exe, server_script, "--no-browser"],
                cwd=script_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info("SuperNova AI server process started")
            
            # Wait for the stop event or process termination
            while True:
                # Check if the process is still running
                if self.process.poll() is not None:
                    logging.error(f"SuperNova AI server process exited with code {self.process.returncode}")
                    break
                
                # Check if the stop event is set
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    logging.info("Stop event received")
                    break
                
                # Read and log output
                stdout_line = self.process.stdout.readline()
                if stdout_line:
                    logging.info(f"Server: {stdout_line.strip()}")
                
                stderr_line = self.process.stderr.readline()
                if stderr_line:
                    logging.error(f"Server error: {stderr_line.strip()}")
                
                time.sleep(1)
            
        except Exception as e:
            logging.error(f"Error running SuperNova AI server: {e}")
        
        logging.info("SuperNova AI service stopped")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SuperNovaAIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SuperNovaAIService)
