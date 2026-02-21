#!/bin/bash
# Build macOS one-file executable using PyInstaller (must run on macOS)
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller
python3 -m PyInstaller --onefile --windowed --name "ActiveReport" generate_report.py
echo "Build complete. See the dist/ folder."
