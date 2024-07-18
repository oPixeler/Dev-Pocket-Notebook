@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python and add it to your system PATH.
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"

python __main__.py

if %errorlevel% neq 0 (
    echo.
    echo The application has closed unexpectedly.
    pause
)