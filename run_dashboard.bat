@echo off
REM ============================================================================
REM Blood Cancer Dashboard - Quick Start Script
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║         🩸 Blood Cancer Analysis Dashboard - Setup & Launch            ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in your PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Step 1: Install requirements
echo 📦 Installing required libraries...
echo This may take 2-3 minutes...
echo.

pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install requirements.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ✅ All libraries installed successfully!
echo.

REM Step 2: Launch Streamlit
echo 🚀 Launching Dashboard...
echo The dashboard will open in your default browser.
echo.

streamlit run dashboard.py

pause
