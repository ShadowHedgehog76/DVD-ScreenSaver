import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import sys

SPEED = 4

def random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

class DVDScreensaver:
    def __init__(self, root):
        self.root = root
        self.root.title("DVD Screensaver")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.root.update_idletasks()
        self.fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        # Load image
        # Support PyInstaller: accès à l'image dans le bundle
        if hasattr(sys, '_MEIPASS'):
            img_path = os.path.join(sys._MEIPASS, "images.png")
        else:
            img_path = os.path.join(os.path.dirname(__file__), "images.png")
        self.original_img = Image.open(img_path).convert("RGBA")
        self.logo_img = ImageTk.PhotoImage(self.original_img)
        self.logo_w, self.logo_h = self.original_img.size
        # Use initial geometry for first position
        initial_width, initial_height = 800, 600
        self.x = random.randint(0, max(0, initial_width - self.logo_w))
        self.y = random.randint(0, max(0, initial_height - self.logo_h))
        self.dx, self.dy = SPEED, SPEED
        self.logo = self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.logo_img)
        self.animate()
        self.root.bind("<Configure>", self.on_resize)
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def on_resize(self, event):
        self.canvas.config(width=event.width, height=event.height)

    def animate(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.x += self.dx
        self.y += self.dy
        hit = False

        # Correction si l'icône sort complètement de l'écran
        if self.x < 0:
            self.x = 0
            self.dx = abs(self.dx)
            hit = True
        elif self.x + self.logo_w > width:
            self.x = max(0, width - self.logo_w)
            self.dx = -abs(self.dx)
            hit = True
        if self.y < 0:
            self.y = 0
            self.dy = abs(self.dy)
            hit = True
        elif self.y + self.logo_h > height:
            self.y = max(0, height - self.logo_h)
            self.dy = -abs(self.dy)
            hit = True
        if hit:
            # Change only white and near-white pixels to a random color, but not black or near-black
            color = random_color()
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            img = self.original_img.copy()
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    pr, pg, pb, pa = pixels[x, y]
                    # Si le pixel est une nuance de blanc (tous les canaux > 160), et pas transparent
                    if min(pr, pg, pb) > 160 and pa > 0:
                        pixels[x, y] = (r, g, b, pa)
            self.logo_img = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.logo, image=self.logo_img)

        self.canvas.coords(self.logo, self.x, self.y)
        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = DVDScreensaver(root)
    root.mainloop()