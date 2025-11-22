@echo off
REM Quick run script for Windows
REM This script verifies setup and runs training

echo ============================================================
echo WATERMARK CNN - QUICK RUN SCRIPT
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Verifying setup...
echo.
python verify_setup.py
if errorlevel 1 (
    echo.
    echo Setup verification failed. Please fix the issues above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 2: Starting training and evaluation...
echo ============================================================
echo.
python train_and_evaluate.py

echo.
echo ============================================================
echo COMPLETE!
echo ============================================================
echo.
echo Results saved to: config_1_baseline\evaluation_results\
echo.
pause
