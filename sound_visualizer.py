import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
import soundcard as sc


class AudioVisualizer:
    def __init__(self, root):
        self.root = root
        root.title("Sound Visualizer")
        root.geometry("850x520")
        self.running = False
        self.recorder = None
        self.samples = np.zeros(2048, dtype=np.float32)

        controls = ttk.Frame(root, padding=12)
        controls.pack(fill="x")
        ttk.Button(controls, text="Start System Audio", command=self.start).pack(side="left")
        ttk.Button(controls, text="Stop", command=self.stop).pack(side="left", padx=6)
        self.status = ttk.Label(
            root,
            text="Visualizes system audio, including Spotify playback.",
            padding=(12, 0),
        )
        self.status.pack(fill="x")
        self.canvas = tk.Canvas(root, background="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.animate()

    def start(self):
        if self.running:
            return
        try:
            self.recorder = sc.default_speaker().recorder(
                samplerate=44100,
                channels=2,
                blocksize=2048,
            )
            self.recorder.__enter__()
            self.running = True
            self.status.config(text="Listening to Windows system audio.")
        except Exception as error:
            self.recorder = None
            messagebox.showerror("Audio capture error", str(error), parent=self.root)
            self.status.config(text="Could not start system audio capture.")

    def stop(self):
        self.running = False
        if self.recorder:
            recorder, self.recorder = self.recorder, None
            try:
                recorder.__exit__(None, None, None)
            except Exception:
                pass
        self.status.config(text="Stopped. Press Start System Audio to listen again.")

    def animate(self):
        if self.running and self.recorder:
            try:
                self.samples = self.recorder.record(numframes=2048).mean(axis=1)
            except Exception as error:
                self.stop()
                messagebox.showerror("Audio capture error", str(error), parent=self.root)

        self.canvas.delete("all")
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if width > 2 and height > 2:
            bars = max(48, width // 9)
            center = height * 0.56
            spectrum = np.abs(np.fft.rfft(self.samples * np.hanning(len(self.samples))))
            spectrum = np.interp(
                np.linspace(0, len(spectrum) - 1, bars),
                np.arange(len(spectrum)),
                spectrum,
            )
            spectrum = np.log1p(spectrum * 12)
            spectrum /= max(float(spectrum.max()), 1.0)

            for index, value in enumerate(spectrum):
                distance = abs(index - bars / 2) / (bars / 2)
                bar_height = max(
                    2,
                    int(height * 0.66 * (1 - 0.56 * distance) * float(value)),
                )
                x = (index + 0.5) * width / bars
                hue = index / max(bars - 1, 1)
                if hue < 0.5:
                    rgb = (
                        int(30 + 40 * hue),
                        int(220 + 35 * hue),
                        int(255 - 180 * hue),
                    )
                else:
                    rgb = (
                        int(70 + 185 * (hue - 0.5) * 2),
                        int(255 - 190 * (hue - 0.5) * 2),
                        40,
                    )
                color = "#%02x%02x%02x" % rgb
                self.canvas.create_rectangle(
                    x - 1, center - bar_height, x + 1, center + bar_height * 0.42,
                    fill=color, outline="",
                )
                self.canvas.create_rectangle(
                    x - 1, center - bar_height - 3, x + 1, center - bar_height - 1,
                    fill="#fff", outline="",
                )
        self.root.after(35, self.animate)

    def close(self):
        self.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    AudioVisualizer(root)
    root.mainloop()
