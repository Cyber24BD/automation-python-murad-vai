@echo off
REM Run Python script using uv
uv run main.py

REM Keep the window open to see the output
if "%ERRORLEVEL%" NEQ "0" (
    echo.
    echo [ERROR] Script failed with error code %ERRORLEVEL%
    pause
) else (
    echo.
    echo [SUCCESS] Script completed successfully
    timeout /t 3 >nul
)
