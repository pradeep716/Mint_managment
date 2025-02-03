@echo off
REM Step 1 Install Python if not installed
echo Checking if Python is installed...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Installing Python...
    REM Download and install Python silently
    curl -o python_installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
) ELSE (
    echo Python is already installed.
)

REM Step 2 Create virtual environment if not exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Step 3 Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Step 4 Install required dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Step 5 Run the Python application in the background (no terminal window)
echo Starting the server...
start /min pythonw app.py

REM Step 6 Wait for the app to initialize 
timeout /t 2 >nul

REM Step 7 Open the sign-up page in the default browser
echo Redirecting to sign-up page...
start http://127.0.0.1:5000

REM Prevent the terminal from staying open
exit
