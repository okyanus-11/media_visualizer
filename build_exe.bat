@echo off
REM Bu komut dist klasorunde MediaVisualizer.exe dosyasini olusturur.
pyinstaller --noconfirm --onefile --windowed --name MediaVisualizer main.py
echo.
echo Hazir: dist\MediaVisualizer.exe
pause

