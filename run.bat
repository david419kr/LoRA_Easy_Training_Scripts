@echo off

title LoRA Trainer
cd %~dp0
call venv\Scripts\activate

set "DEFAULT_PORT=8000"
set "PORT=%DEFAULT_PORT%"
if "%~1"=="" (
    rem no args: use DEFAULT_PORT
) else if /I "%~1"=="--port" (
    if "%~2"=="" goto :port_error
    set "PORT=%~2"
) else if /I "%~1"=="-p" (
    if "%~2"=="" goto :port_error
    set "PORT=%~2"
) else (
    set "PORT=%~1"
)

if not "%PORT%"=="" (
    set "PORT_INVALID="
    for /f "delims=0123456789" %%A in ("%PORT%") do set "PORT_INVALID=1"
    if defined PORT_INVALID goto :port_error
    if %PORT% LSS 1 goto :port_error
    if %PORT% GTR 65535 goto :port_error

    echo Setting backend port to %PORT%
    python -c "import json; from pathlib import Path; p=Path('backend/config.json'); d=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}; d['port']=%PORT%; d.setdefault('remote', False); p.write_text(json.dumps(d, indent=2), encoding='utf-8'); p2=Path('config.json'); d2=json.loads(p2.read_text(encoding='utf-8')) if p2.exists() else {}; d2['backend_url']='http://127.0.0.1:%PORT%'; p2.write_text(json.dumps(d2, indent=2), encoding='utf-8')"
    if errorlevel 1 (
        echo Failed to update port settings.
        pause
        exit /b 1
    )
)

python main.py
pause
exit /b 0

:port_error
echo Invalid or missing port argument.
echo Usage: run.bat [PORT]
echo        run.bat --port PORT
echo        run.bat -p PORT
pause
exit /b 1
