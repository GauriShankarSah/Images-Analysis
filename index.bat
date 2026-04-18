@echo off
setlocal

echo =====================================
echo VENV EXECUTION START (AUTO-REPAIR MODE)
echo =====================================

REM Check venv
IF NOT EXIST venv (
    echo ERROR: Virtual environment not found! Please run setup first.
    pause
    exit /b
)

set VENV_PY=venv\Scripts\python.exe

IF NOT EXIST %VENV_PY% (
    echo ERROR: venv Python missing!
    pause
    exit /b
)

REM =============================
REM AUTO REPAIR SECTION
REM =============================
echo Checking required packages...

%VENV_PY% -c "import torch" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Missing: torch -> reinstalling...
    %VENV_PY% -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
)

%VENV_PY% -c "import flask" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Missing: flask -> reinstalling...
    %VENV_PY% -m pip install flask
)

%VENV_PY% -c "import numpy" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Missing: numpy -> reinstalling...
    %VENV_PY% -m pip install numpy
)

%VENV_PY% -c "import PIL" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Missing: pillow -> reinstalling...
    %VENV_PY% -m pip install pillow
)

%VENV_PY% -c "import faiss" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Missing: faiss-cpu -> reinstalling...
    %VENV_PY% -m pip install faiss-cpu
)

REM CLIP check (important: import name is "clip")
%VENV_PY% -c "import clip" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Missing: CLIP -> reinstalling...
    %VENV_PY% -m pip install git+https://github.com/openai/CLIP.git
)

REM =============================
REM RUN APPLICATION
REM =============================
IF NOT EXIST index.py (
    echo ERROR: index.py not found!
    pause
    exit /b
)

echo Running application...
%VENV_PY% index.py

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Application crashed.
) ELSE (
    echo Application executed successfully.
)

echo =====================================
echo EXECUTION FINISHED (SELF-HEALED)
pause