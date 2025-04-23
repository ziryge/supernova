@echo off
echo ========================================================
echo SuperNova AI Windows Service Installation
echo ========================================================
echo This script will install SuperNova AI as a Windows service
echo that starts automatically when your computer boots.
echo.
echo You need to run this script as Administrator.
echo ========================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: This script must be run as Administrator.
    echo Please right-click on this file and select "Run as administrator".
    echo.
    pause
    exit /b 1
)

REM Check if pywin32 is installed
python -c "import win32serviceutil" >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing pywin32...
    pip install pywin32
    if %errorLevel% neq 0 (
        echo Error: Failed to install pywin32.
        echo Please install it manually: pip install pywin32
        echo.
        pause
        exit /b 1
    )
)

REM Install the service
echo Installing SuperNova AI service...
python windows_service.py install
if %errorLevel% neq 0 (
    echo Error: Failed to install the service.
    echo.
    pause
    exit /b 1
)

REM Start the service
echo Starting SuperNova AI service...
python windows_service.py start
if %errorLevel% neq 0 (
    echo Error: Failed to start the service.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo Installation complete!
echo ========================================================
echo SuperNova AI is now running as a Windows service and will
echo start automatically when your computer boots.
echo.
echo To access SuperNova AI:
echo - Local: http://localhost:8501
echo - Network: http://your_local_ip:8501
echo.
echo Don't forget to set up port forwarding on your router
echo to make SuperNova AI accessible from the internet.
echo ========================================================
echo.

pause
