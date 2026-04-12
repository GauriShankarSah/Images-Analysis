@echo off
setlocal

echo Activating virtual environment...

IF NOT EXIST venv (
    echo Virtual environment not found! Please run setup first.
    pause
    exit /b
)

call venv\Scripts\activate

echo Running app.py...
start http://127.0.0.1:5000
python app.py

pause