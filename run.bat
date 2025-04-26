@echo off
REM --- venv var mi kontrol et ---
if not exist venv (
    echo HATA: venv klasoru bulunamadi.
    echo Lutfen once update.bat calistirin.
    pause
    exit /b 1
)

REM --- Ortami aktif et ve programi calistir ---
echo Ortam aktif ediliyor ve program baslatiliyor...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo HATA: Sanal ortam aktif edilemedi.
    pause
    exit /b 1
)

python anime_bbcode_generator.py
if errorlevel 1 (
    echo HATA: Program calisirken bir hata olustu.
    pause
    exit /b 1
)

exit /b 0