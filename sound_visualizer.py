import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame

class SoundVisualizer:
    def __init__(self, root):
        self.root = root
        root.title("Sound Visualizer")
        root.geometry("850x520")
        self.path = ""
        self.playing = False
        self.paused = False
        self.phase = 0.0
        pygame.mixer.init()
        controls = ttk.Frame(root, padding=12); controls.pack(fill="x")
        ttk.Button(controls, text="Open Audio", command=self.open_audio).pack(side="left")
        ttk.Button(controls, text="Play", command=self.play).pack(side="left", padx=6)
        ttk.Button(controls, text="Pause", command=self.pause).pack(side="left")
        ttk.Button(controls, text="Stop", command=self.stop).pack(side="left", padx=6)
        ttk.Label(controls, text="Volume").pack(side="left", padx=(20,5))
        ttk.Scale(controls, from_=0, to=1, value=.8, command=lambda v: pygame.mixer.music.set_volume(float(v)), length=130).pack(side="left")
        self.status = ttk.Label(root, text="Open an MP3, WAV, OGG, or FLAC file.", padding=(12,0)); self.status.pack(fill="x")
        self.canvas = tk.Canvas(root, background="#000000", highlightthickness=0); self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        root.protocol("WM_DELETE_WINDOW", self.close); self.animate()
    def open_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac"), ("All files", "*.*")])
        if not path: return
        try:
            pygame.mixer.music.load(path); self.path = path; self.status.config(text="Loaded: " + path.replace(chr(92), "/").split("/")[-1]); self.play()
        except pygame.error as e: messagebox.showerror("Audio error", str(e))
    def play(self):
        if not self.path: return self.open_audio()
        pygame.mixer.music.unpause() if self.paused else pygame.mixer.music.play(); self.playing, self.paused = True, False
    def pause(self):
        if self.playing: pygame.mixer.music.pause(); self.paused = True
    def stop(self):
        pygame.mixer.music.stop(); self.playing = self.paused = False
    def animate(self):
        self.canvas.delete("all"); w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 2 and h > 2:
            bars = max(48, w // 9); center = h * .56
            for i in range(bars):
                d = abs(i-bars/2)/(bars/2); e = (1-.56*d)*(.18+.82*abs(math.sin(self.phase+i*.38)))
                if not self.playing or self.paused: e *= .12
                bh = max(2, int(h*.66*e)); x = (i+.5)*w/bars; hue=i/max(bars-1,1)
                if hue < .5: rgb=(int(30+40*hue), int(220+35*hue), int(255-180*hue))
                else: rgb=(int(70+185*(hue-.5)*2), int(255-190*(hue-.5)*2), 40)
                c="#%02x%02x%02x" % rgb; self.canvas.create_rectangle(x-1,center-bh,x+1,center+bh*.42,fill=c,outline=""); self.canvas.create_rectangle(x-1,center-bh-3,x+1,center-bh-1,fill="#fff",outline="")
            self.phase += .16
        self.root.after(35, self.animate)
    def close(self): pygame.mixer.quit(); self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk(); SoundVisualizer(root); root.mainloop()
