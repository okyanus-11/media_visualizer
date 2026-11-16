"""Low-latency system-audio visualizer with background capture and themes."""

import json
import queue
import re
import threading
from pathlib import Path
import tkinter as tk
from tkinter import colorchooser, messagebox, ttk

import numpy as np
import soundcard as sc

from theme import THEMES


class AudioVisualizer:
    def __init__(self, root):
        self.root = root
        root.title("Sound Visualizer")
        root.geometry("900x560")
        root.minsize(620, 400)
        self.running = False
        self._closing = False
        self._stop_event = threading.Event()
        self._samples_lock = threading.Lock()
        self._capture_thread = None
        self._ui_queue = queue.SimpleQueue()
        self.samples = np.zeros(2048, dtype=np.float32)
        self._settings_path = Path.home() / ".media-visualizer.json"
        self._preferences = self._load_preferences()
        self.theme_name = self._preferences.get("theme", "graphite")
        if self.theme_name not in THEMES:
            self.theme_name = "graphite"
        self.accent = self._preferences.get("accent", THEMES[self.theme_name]["accent"])
        if not isinstance(self.accent, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", self.accent):
            self.accent = THEMES[self.theme_name]["accent"]

        controls = ttk.Frame(root, padding=14)
        controls.pack(fill="x")
        self.start_button = ttk.Button(controls, text="Start System Audio", command=self.start)
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(controls, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=6)
        ttk.Label(controls, text="Theme").pack(side="left", padx=(18, 5))
        self.theme_select = ttk.Combobox(
            controls, state="readonly", width=10, values=("Graphite", "Midnight", "Light")
        )
        self.theme_select.set(self.theme_name.title())
        self.theme_select.pack(side="left")
        self.theme_select.bind("<<ComboboxSelected>>", self._theme_selected)
        ttk.Button(controls, text="Accent", command=self.choose_accent).pack(side="left", padx=6)

        self.status = ttk.Label(
            root, text="System audio is captured in a background thread.", padding=(14, 0)
        )
        self.status.pack(fill="x")
        self.canvas = tk.Canvas(root, background="#171f2a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=14, pady=14)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.apply_theme()
        self.animate()

    def _load_preferences(self):
        try:
            data = json.loads(self._settings_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def _save_preferences(self):
        temp = self._settings_path.with_suffix(".tmp")
        try:
            temp.write_text(json.dumps({"theme": self.theme_name, "accent": self.accent}, indent=2), encoding="utf-8")
            temp.replace(self._settings_path)
        except OSError:
            temp.unlink(missing_ok=True)

    def apply_theme(self):
        palette = dict(THEMES[self.theme_name])
        palette["accent"] = self.accent
        style = ttk.Style(self.root)
        style.theme_use("clam")
        self.root.configure(background=palette["background"])
        style.configure("TFrame", background=palette["background"])
        style.configure("TLabel", background=palette["background"], foreground=palette["muted"], font=("Segoe UI", 10))
        style.configure("TButton", background=palette["surface_alt"], foreground=palette["text"], bordercolor=palette["border"], padding=(9, 6))
        style.map("TButton", background=[("active", palette["border"])])
        style.configure("TCombobox", fieldbackground=palette["surface_alt"], background=palette["surface_alt"], foreground=palette["text"], bordercolor=palette["border"], padding=5)
        self.canvas.configure(background=palette["surface"])
        self._save_preferences()

    def _theme_selected(self, _event=None):
        self.theme_name = self.theme_select.get().lower()
        self.accent = THEMES[self.theme_name]["accent"]
        self.apply_theme()

    def choose_accent(self):
        selected = colorchooser.askcolor(color=self.accent, parent=self.root, title="Choose accent colour")[1]
        if selected:
            self.accent = selected
            self.apply_theme()

    def _post_to_ui(self, callback):
        # Tk widgets are touched only by the main thread; the capture worker
        # communicates through this thread-safe queue.
        if not self._closing:
            self._ui_queue.put(callback)

    def start(self):
        if self.running:
            return
        self._stop_event.clear()
        self.running = True
        self.start_button.configure(state="disabled")
        self.status.config(text="Connecting to the default speaker…")
        self._capture_thread = threading.Thread(
            target=self._capture_loop, name="audio-capture", daemon=True
        )
        self._capture_thread.start()

    def _capture_loop(self):
        recorder = None
        error = None
        try:
            recorder = sc.default_speaker().recorder(
                samplerate=44100, channels=2, blocksize=2048
            )
            recorder.__enter__()
            self._post_to_ui(lambda: self.status.config(text="Listening to system audio."))
            while not self._stop_event.is_set():
                chunk = recorder.record(numframes=2048).mean(axis=1)
                with self._samples_lock:
                    self.samples = chunk.astype(np.float32, copy=False)
        except Exception as exc:
            error = str(exc)
        finally:
            if recorder is not None:
                try:
                    recorder.__exit__(None, None, None)
                except Exception:
                    pass
            self.running = False
            self._post_to_ui(lambda: self._capture_finished(error))

    def _capture_finished(self, error):
        if self._closing:
            return
        self.start_button.configure(state="normal")
        if error:
            self.status.config(text="Audio capture failed.")
            messagebox.showerror("Audio capture error", error, parent=self.root)
        else:
            self.status.config(text="Stopped. Press Start System Audio to listen again.")

    def stop(self):
        if not self.running:
            return
        self._stop_event.set()
        self.status.config(text="Stopping audio capture…")

    def animate(self):
        if self._closing:
            return
        while not self._ui_queue.empty():
            try:
                self._ui_queue.get_nowait()()
            except queue.Empty:
                break
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if width > 2 and height > 2:
            with self._samples_lock:
                samples = self.samples.copy()
            spectrum = np.abs(np.fft.rfft(samples * np.hanning(len(samples))))
            bars = min(128, max(32, width // 8))
            spectrum = np.interp(
                np.linspace(0, len(spectrum) - 1, bars),
                np.arange(len(spectrum)),
                spectrum,
            )
            spectrum = np.log1p(spectrum * 12)
            peak = max(float(spectrum.max()), 1.0)
            spectrum = spectrum / peak
            self.canvas.delete("spectrum")
            center = height * 0.56
            for index, value in enumerate(spectrum):
                distance = abs(index - bars / 2) / max(bars / 2, 1)
                bar_height = max(2, int(height * 0.66 * (1 - 0.56 * distance) * float(value)))
                x = (index + 0.5) * width / bars
                self.canvas.create_rectangle(
                    x - 2, center - bar_height, x + 2, center + bar_height * 0.42,
                    fill=self.accent, outline="", tags="spectrum",
                )
        self.root.after(33, self.animate)

    def close(self):
        self._closing = True
        self._stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    AudioVisualizer(root)
    root.mainloop()
