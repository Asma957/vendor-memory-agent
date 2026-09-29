@echo off
setlocal
cd /d "%~dp0"
title Vendor Memory Agent
echo.
echo ===== Vendor Memory Agent: one-click start =====

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install it from python.org and tick "Add to PATH".
  pause
  exit /b 1
)

if not exist venv\Scripts\activate.bat (
  echo [1/5] Creating virtual environment...
  python -m venv venv
  if errorlevel 1 goto :fail
)
call venv\Scripts\activate.bat

if not exist .env copy .env.example .env >nul

findstr /C:"your-hindsight-key" /C:"your-groq-key" .env >nul
if not errorlevel 1 (
  echo.
  echo [2/5] Add your API keys. Notepad is opening.
  echo       Paste the real keys after HINDSIGHT_API_KEY and GROQ_API_KEY, save, then close Notepad.
  start /wait notepad .env
  findstr /C:"your-hindsight-key" /C:"your-groq-key" .env >nul
  if not errorlevel 1 (
    echo The keys are still placeholders. Add them and run run.bat again.
    pause
    exit /b 1
  )
)

if not exist venv\.deps_ok (
  echo [3/5] Installing libraries. The first time takes 2-3 minutes...
  python -m pip install -r requirements.txt
  if errorlevel 1 goto :fail
  echo ok> venv\.deps_ok
)

if not exist venv\.conn_ok (
  echo [4/5] Checking Hindsight and Groq connections...
  python test_connection.py
  if errorlevel 1 goto :fail
  echo ok> venv\.conn_ok
)

echo [5/5] Checking demo data and starting the app...
python seed.py
if errorlevel 1 goto :fail

streamlit run app.py
goto :eof

:fail
echo.
echo Something failed. Copy the error above and send it to Claude.
pause
exit /b 1
