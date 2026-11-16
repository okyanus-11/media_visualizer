# Media Visualizer

A lightweight Tkinter desktop app for image filters and live system-audio
visualization.

## Image Visualizer

Open PNG, JPG or JPEG files, apply grayscale, sepia, negative and brightness
adjustments, then save the result. Filter rendering is debounced so rapid
slider movement does not trigger a full image render for every intermediate
value.

Choose Graphite, Midnight or Light, then use **Accent** to pick any accent
colour. Preferences are saved locally.

## Sound Visualizer

The Sound Visualizer captures the default Windows speaker output through
WASAPI loopback and renders a CAVA-inspired spectrum. Audio capture runs in a
background thread; the Tkinter interface remains on its main thread and
updates the spectrum at approximately 30 FPS.

It has the same saved theme and custom accent controls.

Install image dependencies and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

For the Sound Visualizer, install its separate dependencies and run:

```powershell
pip install -r sound_requirements.txt
python sound_visualizer.py
```

Build standalone Windows executables with PyInstaller:

```powershell
python -m PyInstaller --noconfirm --onefile --windowed --name MediaVisualizer main.py
python -m PyInstaller --noconfirm --onefile --windowed --name SoundVisualizer sound_visualizer.py
```

## Installation

Requires Python 3.10+ and Tkinter. Install `requirements.txt` and run `python main.py` for image visualization. The separate live sound visualizer uses Windows WASAPI loopback: install `sound_requirements.txt` and run `python sound_visualizer.py`. See the [full installation guide](INSTALLATION.md) for setup and optional executable builds.
