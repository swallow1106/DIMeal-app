@echo off
:: Change directory to the batch file's location
cd /d "%~dp0"

echo ===================================================
echo   JFFD DIY Meal Prep Calculator Local Starter 🐶
echo ===================================================
echo.

:: Check if virtual environment exists
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Please make sure Python is installed and added to PATH.
        pause
        exit /b
    )
)

:: Activate the virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install/Upgrade dependencies
echo [INFO] Installing/verifying requirements (Streamlit, Pandas)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

:: Run the Streamlit application
echo.
echo [INFO] Starting JFFD DIY Meal Prep Calculator...
echo.
streamlit run streamlit_app.py

:: If Streamlit crashes or stops, pause so the error traceback is visible
echo.
echo [INFO] Streamlit server has stopped.
pause
