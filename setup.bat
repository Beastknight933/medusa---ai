@echo off
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Copy .env file (works like cp in Linux)
copy .env.template .env

REM Run the script
python trial_main.py

pause
 