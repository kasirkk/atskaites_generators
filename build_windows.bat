@echo off
REM Build Windows one-file executable using PyInstaller
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name ActiveReport generate_report.py
echo Build complete. The exe will be in the dist\ folder.
pause
