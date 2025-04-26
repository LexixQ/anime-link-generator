@echo off
echo Starting update process...

REM --- Python Check ---
py -3 --version > nul 2>&1
if errorlevel 1 (
    echo ERROR Python 3 not found or not in PATH.
    echo Install Python 3 from python.org and add to PATH.
    pause
    exit /b 1
) else (
    echo Python 3 OK.
)

REM --- Venv Check / Create ---
if not exist venv (
    echo Creating venv...
    py -3 -m venv venv
    if errorlevel 1 (
        echo ERROR Cannot create venv.
        pause
        exit /b 1
    )
    echo venv created OK.
) else (
    echo venv already exists.
)

REM --- Install Packages ---
echo Installing packages from requirements.txt...
call venv\Scripts\activate.bat && pip install -r requirements.txt --no-cache-dir
if errorlevel 1 (
    echo ERROR Cannot install packages. Check internet or requirements.txt.
    pause
    exit /b 1
)

echo.
echo Setup complete.
echo Run run.bat to start.
echo.
pause
exit /b 0