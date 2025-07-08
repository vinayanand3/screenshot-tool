import tkinter as tk
from PIL import Image, ImageTk
import mss

class Magnifier:
    def __init__(self, parent, settings, total_left, total_top, total_width, total_height):
        self.parent = parent
        self.settings = settings
        self.total_left = total_left
        self.total_top = total_top
        self.total_width = total_width
        self.total_height = total_height
        self.window = None
        self.canvas = None
        self.create_magnifier()

    def create_magnifier(self):
        if self.window:
            self.window.destroy()
        self.window = tk.Toplevel(self.parent)
        self.window.title("Magnifier")
        self.window.geometry(f"{self.settings['magnifier_size']}x{self.settings['magnifier_size']}")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg='black')
        self.canvas = tk.Canvas(
            self.window,
            width=self.settings['magnifier_size'],
            height=self.settings['magnifier_size'],
            bg='black',
            highlightthickness=2,
            highlightbackground='white'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.geometry(f"+{self.total_left + 100}+{self.total_top + 100}")

    def update_magnifier(self, x, y):
        if not self.window or not self.canvas:
            return
        try:
            with mss.mss() as sct:
                zoom = self.settings['magnifier_zoom']
                size = self.settings['magnifier_size']
                capture_size = size // zoom
                screen_x = int(x) + self.total_left
                screen_y = int(y) + self.total_top
                left = max(0, screen_x - capture_size // 2)
                top = max(0, screen_y - capture_size // 2)
                right = min(self.total_width, left + capture_size)
                bottom = min(self.total_height, top + capture_size)
                if right - left < capture_size:
                    left = max(0, right - capture_size)
                if bottom - top < capture_size:
                    top = max(0, bottom - capture_size)
                monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
                img = sct.grab(monitor)
                pil_img = Image.frombytes("RGB", img.size, img.rgb)
                pil_img = pil_img.resize((size, size), Image.Resampling.NEAREST)
                photo = ImageTk.PhotoImage(pil_img)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=photo, anchor="nw")
                self.canvas.image = photo
                center = size // 2
                self.canvas.create_line(center, 0, center, size, fill='red', width=1)
                self.canvas.create_line(0, center, size, center, fill='red', width=1)
                mag_x = screen_x + 20
                mag_y = screen_y + 20
                if mag_x + size > self.total_width:
                    mag_x = screen_x - size - 20
                if mag_y + size > self.total_height:
                    mag_y = screen_y - size - 20
                self.window.geometry(f"+{mag_x}+{mag_y}")
        except Exception:
            pass

    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None
            self.canvas = None 