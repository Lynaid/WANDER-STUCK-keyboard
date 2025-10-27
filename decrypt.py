import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

KEY_SIZE = (64, 64)
IMG_DIR = Path("img")

mapping = {
    'q': 'q','w': 'w','e': 'e','r': 'r','t': 't','y': 'y','u': 'u','i': 'i','o': 'o','p': 'p',
    'a': 'a','s': 's','d': 'd','f': 'f','g': 'g','h': 'h','j': 'j','k': 'k','l': 'l',';': ';',
    'z': 'z','x': 'x','c': 'c','v': 'v','b': 'b','n': 'n','m': 'm',',': ',','.': '.','/': '/'
}

shift_on = False
images = {}
buttons = {}

def load_resized_image(path):
    """Loads and scales PNGs"""
    img = Image.open(path).convert("RGBA")
    img = img.resize(KEY_SIZE, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def press(key):
    global shift_on
    if key == "Shift":
        shift_on = not shift_on
        update_keyboard()
        return
    elif key == "Space":
        text_box.insert(tk.END, " ")
        return
    elif key == "Enter":
        text_box.insert(tk.END, "\n")
        return

    out = mapping.get(key.lower(), key)
    if shift_on:
        out = out.upper()
    text_box.insert(tk.END, out)

def update_keyboard():
    for k, btn in buttons.items():
        if k in ["Shift", "Space", "Enter"]:
            continue
        img_name = f"{k.upper()}_key.png" if shift_on else f"S{k.upper()}_key.png"
        img_path = IMG_DIR / img_name
        if img_path.exists():
            images[k] = load_resized_image(img_path)
            btn.config(image=images[k], text="")
        else:
            btn.config(image="", text=k.upper() if shift_on else k.lower())

root = tk.Tk()
root.title("Virtual keyboard")

text_box = tk.Text(root, height=3, width=50)
text_box.pack(pady=10)

rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
for row in rows:
    frame = tk.Frame(root)
    frame.pack(pady=2)
    for k in row:
        img_name = f"S{k.upper()}_key.png"
        img_path = IMG_DIR / img_name
        if img_path.exists():
            images[k] = load_resized_image(img_path)
            btn = tk.Button(frame, image=images[k], command=lambda x=k: press(x), borderwidth=0)
        else:
            btn = tk.Button(frame, text=k, width=5, height=2, command=lambda x=k: press(x))
        btn.pack(side=tk.LEFT, padx=2)
        buttons[k] = btn

extra = tk.Frame(root)
extra.pack(pady=4)

for key in ["Shift", "Space", "Enter"]:
    btn = tk.Button(extra, text=key, width=8, height=2, command=lambda x=key: press(x))
    btn.pack(side=tk.LEFT, padx=3)
    buttons[key] = btn

root.mainloop()
