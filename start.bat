@echo off
cd /d "%~dp0"
if not exist venv (
    echo Virtual environment not found! Setting it up...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

start "" /B venv\Scripts\pythonw.exe converter.py
