@echo off
setlocal
title Etiket Sistemi
cd /d "%~dp0"
if errorlevel 1 goto :error

if not exist ".venv\Scripts\python.exe" (
    echo Ilk kullanim icin kurulum baslatiliyor...
    call "%~dp0kurulum.bat"
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -c "import flask, reportlab" >nul 2>&1
if errorlevel 1 (
    echo Kutuphaneler eksik. Kurulum tekrar baslatiliyor...
    call "%~dp0kurulum.bat"
    if errorlevel 1 goto :error
)

if not defined PORT set "PORT=5000"
echo.
echo Uygulama aciliyor: http://127.0.0.1:%PORT%/
echo Bu pencere acik kaldigi surece uygulama calisir.
echo.
".venv\Scripts\python.exe" "app.py"
echo.
echo Uygulama durdu. Hata varsa yukaridaki mesaji kontrol edin.
pause
exit /b 0

:error
echo.
echo Uygulama baslatilamadi.
pause
exit /b 1
