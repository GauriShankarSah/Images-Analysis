@echo off
setlocal enabledelayedexpansion

echo =====================================
echo Checking Python 3.13 installation...
echo =====================================

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    set PYTHON_MISSING=1
) ELSE (
    for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PY_VER=%%V

    echo Detected Python version: !PY_VER! | findstr "3.13" >nul
    IF %ERRORLEVEL% NEQ 0 (
        set PYTHON_MISSING=1
    ) ELSE (
        set PYTHON_MISSING=0
    )
)

IF "%PYTHON_MISSING%"=="1" (
    echo Installing Python 3.13...

    curl -L -o python-installer.exe https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    echo Python installed. PLEASE RESTART terminal and run again.
    pause
    exit /b
)

echo =====================================
echo Downloading project from GitHub...
echo =====================================

set ZIP=project.zip
set FOLDER=Images-Analysis-main

IF EXIST %ZIP% del %ZIP%
IF EXIST %FOLDER% rmdir /s /q %FOLDER%

curl -L -o %ZIP% https://github.com/GauriShankarSah/Images-Analysis/archive/refs/heads/main.zip

powershell -command "Expand-Archive -Force '%ZIP%' -DestinationPath ."

echo =====================================
echo Entering project folder...
echo =====================================

cd %FOLDER%

echo =====================================
echo Creating virtual environment...
echo =====================================

IF NOT EXIST venv (
    python -m venv venv
)

call venv\Scripts\activate

echo =====================================
echo Upgrading pip...
echo =====================================

python -m pip install --upgrade pip

echo =====================================
echo Installing dependencies...
echo =====================================

IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found! Installing fallback packages...
    pip install flask pillow numpy torch torchvision faiss-cpu
)

echo =====================================
echo SETUP COMPLETED SUCCESSFULLY 🚀
echo =====================================

pause