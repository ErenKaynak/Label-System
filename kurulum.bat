@echo off
setlocal
title Etiket Sistemi Kurulum
cd /d "%~dp0"
if errorlevel 1 goto :error

set "PYTHON_CMD="
py -3 -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
    python -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)
if not defined PYTHON_CMD (
    echo Python 3.9 veya ustu bulunamadi.
    echo Python'u python.org adresinden kurup bu dosyayi tekrar calistirin.
    goto :error
)

echo Proje icin sanal Python ortami olusturuluyor...
%PYTHON_CMD% -m venv ".venv"
if errorlevel 1 goto :error

echo Gerekli kutuphaneler kuruluyor...
".venv\Scripts\python.exe" -m ensurepip --upgrade
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r "requirements.txt"
if errorlevel 1 goto :error

echo.
echo Kurulum tamamlandi. baslat.bat dosyasini acin.
pause
exit /b 0

:error
echo.
echo Kurulum tamamlanamadi. Yukaridaki hata mesajini kontrol edin.
pause
exit /b 1
