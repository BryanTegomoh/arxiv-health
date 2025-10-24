@echo off
REM Quick Start Script for arXiv Health Monitor (Windows)

echo ======================================================================
echo arXiv Health Monitor - Quick Start
echo ======================================================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env and add your API key:
    echo    copy .env.example .env
    echo Then edit .env and add your Gemini API key.
    echo.
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Running arXiv Health Monitor...
python run.py

echo.
echo [3/3] Opening website...
start docs\index.html

echo.
echo ======================================================================
echo Done! Your website should open in your browser.
echo ======================================================================
pause
