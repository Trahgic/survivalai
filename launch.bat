@echo off
setlocal

echo.
echo  SurvivalAI — Offline Survival Assistant
echo  =========================================
echo.

set "DRIVE_ROOT=%~dp0"
set "SERVER=%DRIVE_ROOT%engine\win-x64\llama-server.exe"
set "MODEL=%DRIVE_ROOT%model\llama-3.1-8b-q4_k_m.gguf"
set "UI_DIR=%DRIVE_ROOT%ui"
set "HISTORY_DIR=%DRIVE_ROOT%history"
set "PORT=8090"

if not exist "%SERVER%" (
    echo [ERROR] Server binary not found at: %SERVER%
    echo.
    echo Open ui\fallback.html in your browser for keyword search.
    pause
    exit /b 1
)

if not exist "%MODEL%" (
    echo [ERROR] Model file not found at: %MODEL%
    pause
    exit /b 1
)

if not exist "%HISTORY_DIR%" mkdir "%HISTORY_DIR%"

echo  Starting server on http://localhost:%PORT%
echo  Press Ctrl+C to stop.
echo.

start http://localhost:%PORT%

"%SERVER%" ^
    --model "%MODEL%" ^
    --ctx-size 4096 ^
    --threads 4 ^
    --port %PORT% ^
    --host 127.0.0.1 ^
    --path "%UI_DIR%"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server failed to start.
    echo.
    echo Common causes:
    echo   - Not enough RAM (need ~6 GB free)
    echo   - Another program using port %PORT%
    echo   - Antivirus blocking the executable
    echo.
    echo Fallback: open ui\fallback.html in your browser.
    pause
)

endlocal
