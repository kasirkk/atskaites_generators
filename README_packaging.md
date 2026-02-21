Packaging instructions

Overview
- This project is a Python Tkinter/Plotly script: `generate_report.py`.
- You can produce a standalone Windows `.exe` using PyInstaller on Windows.
- For macOS, build must be performed on a Mac (PyInstaller cannot reliably cross-compile macOS apps from Windows).

Quick Windows build (recommended)
1. Open PowerShell in the project folder.
2. (Optional) Create and activate a venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install deps and build:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name ActiveReport generate_report.py
```

4. The generated `ActiveReport.exe` will be in `dist\ActiveReport.exe`.

Notes for macOS
- Run the `build_mac.sh` script on a Mac (make it executable: `chmod +x build_mac.sh`).
- macOS builds may require codesigning and notarization for distribution.
- Use `python3` and ensure you build on the desired target macOS version.

Caveats
- PyInstaller bundles Python and dependencies; resulting exe can be large.
- If your script uses dynamic imports or non-Python assets, you may need `--add-data` or a `.spec` file.
- For Tkinter GUI, use `--windowed` to suppress console.

If you want, I can now attempt to run the Windows build here (this environment is Windows). Reply "Build now" to let me run it, or "Only prepare scripts" to stop here.