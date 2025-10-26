@echo off
title Etiket Sistemi Kurulum Sihirbazi
echo:
echo   ***********************************************************
echo   * *
echo   * Etiket Sistemi Icin Gerekli Kutuphaneler Kuruluyor    *
echo   * *
echo   ***********************************************************
echo:
echo  Bu script, Python'un kendi icinden pip'i bulup guncelleyecek
echo  ve gerekli kutuphaneleri (flask, reportlab) yukleyecektir.
echo:
echo  Lutfen internet baglantinizin oldugundan emin olun.
echo:
echo  -----------------------------------------------------------
echo   [ADIM 1] pip (Python Paket Yoneticisi) guncelleniyor...
echo  -----------------------------------------------------------
echo:

:: 'py -m ensurepip' komutu, Python'un kendi icindeki pip'i bulup kurmasini/guncellemesini saglar.
py -m ensurepip --upgrade

echo:
echo  -----------------------------------------------------------
echo   [ADIM 2] Gerekli kutuphaneler (flask, reportlab) yukleniyor...
echo  -----------------------------------------------------------
echo:

:: 'py -m pip install' komutu, 'pip' komutu PATH'de olmasa bile
:: dogrudan Python uzerinden pip'i calistirir. En saglam yontem budur.
py -m pip install flask reportlab

echo:
echo  -----------------------------------------------------------
echo   KURULUM TAMAMLANDI!
echo  -----------------------------------------------------------
echo:
echo   'flask' ve 'reportlab' kutuphaneleri basariyla kuruldu.
echo:
echo   Artik 'app-test.py' dosyasini calistirabilirsiniz.
echo   Bu pencereyi kapatabilirsiniz.
echo:
pause