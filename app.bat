@echo off
setlocal

echo =====================================
echo ACTIVATING VIRTUAL ENVIRONMENT
echo =====================================

IF NOT EXIST venv (
    echo Virtual environment not found! Please run setup first.
    pause
    exit /b
)

call venv\Scripts\activate

REM =============================
REM CHECK APP FILE
REM =============================
IF NOT EXIST app.py (
    echo ERROR: app.py not found in current directory!
    pause
    exit /b
)

REM =============================
REM START SERVER MESSAGE
REM =============================
echo =====================================
echo STARTING FLASK APP...
echo =====================================

echo Opening browser at http://127.0.0.1:5000 ...
start "" http://127.0.0.1:5000

REM =============================
REM RUN APP
REM =============================
python app.py

REM =============================
REM ERROR CHECK
REM =============================
IF %ERRORLEVEL% NEQ 0 (
    echo =====================================
    echo ERROR: Application crashed or stopped unexpectedly
    echo =====================================
) ELSE (
    echo =====================================
    echo APPLICATION STOPPED NORMALLY
    echo =====================================
)

pause