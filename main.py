"""Basit görsel görselleştirici uygulaması."""

import json
import re
from pathlib import Path
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

from PIL import Image, ImageEnhance, ImageOps, ImageTk

from theme import THEMES


class MediaVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Visualizer")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)

        self.original_image = None
        self.current_image = None
        self.photo_image = None  # Tkinter resmi bellekten silmesin diye saklanır.
        self.image_path = ""
        self._render_job = None
        self._settings_path = Path.home() / ".media-visualizer.json"
        self._preferences = self._load_preferences()
        self.theme_name = self._preferences.get("theme", "graphite")
        if self.theme_name not in THEMES:
            self.theme_name = "graphite"
        self.accent = self._preferences.get("accent", THEMES[self.theme_name]["accent"])
        if not isinstance(self.accent, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", self.accent):
            self.accent = THEMES[self.theme_name]["accent"]

        self.create_widgets()
        self.apply_theme()

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
        style.configure("TLabel", background=palette["background"], foreground=palette["text"], font=("Segoe UI", 10))
        style.configure("TButton", background=palette["surface_alt"], foreground=palette["text"], bordercolor=palette["border"], padding=(9, 6))
        style.map("TButton", background=[("active", palette["border"])])
        style.configure("TCombobox", fieldbackground=palette["surface_alt"], background=palette["surface_alt"], foreground=palette["text"], bordercolor=palette["border"], padding=5)
        style.configure("Horizontal.TScale", background=palette["background"], troughcolor=palette["surface_alt"])
        self.canvas.configure(background=palette["surface"])
        self.info_label.configure(foreground=palette["muted"])
        self._save_preferences()

    def _theme_selected(self, _event=None):
        previous_default = THEMES[self.theme_name]["accent"]
        self.theme_name = self.theme_select.get().lower()
        if self.accent.lower() == previous_default.lower():
            self.accent = THEMES[self.theme_name]["accent"]
        self.apply_theme()

    def choose_accent(self):
        selected = colorchooser.askcolor(color=self.accent, parent=self.root, title="Choose accent colour")[1]
        if selected:
            self.accent = selected
            self.apply_theme()

    def _schedule_changes(self):
        if self._render_job is not None:
            self.root.after_cancel(self._render_job)
        self._render_job = self.root.after(90, self._apply_scheduled_changes)

    def _apply_scheduled_changes(self):
        self._render_job = None
        self.apply_changes()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding=12)
        top_frame.pack(fill="x")

        ttk.Button(top_frame, text="Görsel Aç", command=self.open_image).pack(side="left")
        ttk.Button(top_frame, text="Orijinale Dön", command=self.reset_image).pack(side="left", padx=8)
        ttk.Button(top_frame, text="Kaydet", command=self.save_image).pack(side="left")

        ttk.Label(top_frame, text="Theme:").pack(side="left", padx=(18, 5))
        self.theme_select = ttk.Combobox(top_frame, state="readonly", width=10, values=("Graphite", "Midnight", "Light"))
        self.theme_select.set(self.theme_name.title())
        self.theme_select.pack(side="left")
        self.theme_select.bind("<<ComboboxSelected>>", self._theme_selected)
        ttk.Button(top_frame, text="Accent", command=self.choose_accent).pack(side="left", padx=(6, 0))

        ttk.Label(top_frame, text="Filtre:").pack(side="left", padx=(18, 5))
        self.filter_name = tk.StringVar(value="Normal")
        filter_menu = ttk.Combobox(
            top_frame,
            textvariable=self.filter_name,
            values=["Normal", "Siyah Beyaz", "Sepya", "Negatif"],
            state="readonly",
            width=14,
        )
        filter_menu.pack(side="left")
        filter_menu.bind("<<ComboboxSelected>>", lambda event: self._schedule_changes())

        self.brightness = tk.DoubleVar(value=1.0)
        ttk.Label(top_frame, text="Parlaklık").pack(side="left", padx=(25, 5))
        ttk.Scale(
            top_frame,
            from_=0.3,
            to=2.0,
            variable=self.brightness,
            command=lambda value: self._schedule_changes(),
            length=130,
        ).pack(side="left")

        self.info_label = ttk.Label(self.root, text="Bir PNG, JPG veya JPEG görsel seçin.", padding=(12, 0))
        self.info_label.pack(fill="x")

        # Görsel alanı pencere büyüyüp küçülünce ortada kalır.
        self.canvas = tk.Canvas(self.root, background="#171f2a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda event: self.show_image())

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Görsel seçin",
            filetypes=[("Görsel dosyaları", "*.png *.jpg *.jpeg"), ("Tüm dosyalar", "*.*")],
        )
        if not path:
            return

        try:
            # convert ile şeffaf PNG ve farklı renk modları sorunsuz gösterilir.
            self.original_image = Image.open(path).convert("RGB")
            self.image_path = path
            self.filter_name.set("Normal")
            self.brightness.set(1.0)
            self.apply_changes()
            self.info_label.config(text=f"Yüklendi: {path.split('/')[-1]}")
        except Exception as error:
            messagebox.showerror("Dosya hatası", f"Görsel açılamadı.\n\n{error}")

    def apply_changes(self):
        if self.original_image is None:
            return

        image = self.original_image.copy()
        selected_filter = self.filter_name.get()

        if selected_filter == "Siyah Beyaz":
            image = ImageOps.grayscale(image).convert("RGB")
        elif selected_filter == "Sepya":
            # Basit sepya etkisi için siyah-beyaz resme sıcak renk katılır.
            grayscale = ImageOps.grayscale(image)
            image = ImageOps.colorize(grayscale, "#3b2a17", "#f4d9a6")
        elif selected_filter == "Negatif":
            image = ImageOps.invert(image)

        self.current_image = ImageEnhance.Brightness(image).enhance(self.brightness.get())
        self.show_image()

    def show_image(self):
        if self.current_image is None or self.canvas.winfo_width() < 2:
            return

        # Görseli en-boy oranını koruyarak canvas'a sığdır.
        max_width = max(self.canvas.winfo_width() - 30, 1)
        max_height = max(self.canvas.winfo_height() - 30, 1)
        preview = self.current_image.copy()
        preview.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.photo_image,
            anchor="center",
        )

    def reset_image(self):
        if self.original_image is None:
            return
        self.filter_name.set("Normal")
        self.brightness.set(1.0)
        self.apply_changes()
        self.info_label.config(text="Orijinal görsele dönüldü.")

    def save_image(self):
        if self.current_image is None:
            messagebox.showinfo("Görsel yok", "Önce bir görsel açmalısınız.")
            return

        path = filedialog.asksaveasfilename(
            title="Düzenlenmiş görseli kaydet",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
        )
        if not path:
            return

        try:
            self.current_image.save(path)
            self.info_label.config(text=f"Kaydedildi: {path}")
        except Exception as error:
            messagebox.showerror("Kaydetme hatası", f"Görsel kaydedilemedi.\n\n{error}")


if __name__ == "__main__":
    window = tk.Tk()
    MediaVisualizerApp(window)
    window.mainloop()

