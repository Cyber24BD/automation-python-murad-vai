@echo off
rem -------------------------------------------------------------
rem Run FastAPI backend on Windows.
rem 1. Tries to start on DEFAULT_PORT (8000).
rem 2. If the port is already in use, falls back to a random free port.
rem 3. Prints the port number so you can open it in your browser.
rem -------------------------------------------------------------

setlocal ENABLEDELAYEDEXPANSION

:: Attempt to activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment venv not found. Running with system Python.
)

:: Module path to your FastAPI application
set APP_MODULE=fastapi_crud.main:app

:: Preferred port. Change this if you want another default.
set DEFAULT_PORT=8510
set PORT=%DEFAULT_PORT%

:: Check if DEFAULT_PORT is currently LISTENING
netstat -an | findstr ":%PORT% " | find "LISTENING" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Port %PORT% is already in use. Selecting a random alternative...
    :: Generate a pseudo-random port between 10000 and 60000
    set /a PORT=%RANDOM% + 10000
)

echo Starting server on port %PORT% . . .
python -m uvicorn %APP_MODULE% --host 0.0.0.0 --port %PORT%

pause
