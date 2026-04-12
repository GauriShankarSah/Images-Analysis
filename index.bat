@echo off
setlocal

echo Activating virtual environment...

IF NOT EXIST venv (
    echo Virtual environment not found! Please run setup first.
    pause
    exit /b
)

call venv\Scripts\activate

echo Running index.py...
python index.py

pause