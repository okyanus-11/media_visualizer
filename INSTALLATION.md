# Installation

## Requirements
- Python 3.10 or newer
- Windows is required for the system-audio visualizer (WASAPI loopback)
- Tkinter support for the desktop interface

## Image Visualizer

Windows (PowerShell):

```powershell
git clone https://github.com/okyanus-11/media_visualizer.git
cd media_visualizer
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Linux: install Tkinter for your Python version (for example, `python3-tk`), then create and activate a virtual environment, install `requirements.txt`, and run `python main.py`.

## Sound Visualizer (Windows)

With the same virtual environment activated:

```powershell
pip install -r sound_requirements.txt
python sound_visualizer.py
```

The sound visualizer captures the default Windows playback device. It does not record microphone input.

## Optional standalone executables

Install the dependencies above, then run:

```powershell
python -m PyInstaller --noconfirm --onefile --windowed --name MediaVisualizer main.py
python -m PyInstaller --noconfirm --onefile --windowed --name SoundVisualizer sound_visualizer.py
```

Executables are written to `dist\`. Build each target on the operating system where it will run.
