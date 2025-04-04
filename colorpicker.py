import tkinter as tk
import threading
import mss
import numpy as np
from pynput import mouse

is_picking = False

def exit_app():
    root.quit()

def get_average_color(x, y, size=3):
    with mss.mss() as sct:
        monitor = sct.monitors[0]  
        screenshot = sct.grab(monitor)

        pixel_x = x - monitor["left"]
        pixel_y = y - monitor["top"]

        pixels = []
        for dx in range(-size//2, size//2 + 1):
            for dy in range(-size//2, size//2 + 1):
                try:
                    r, g, b = screenshot.pixel(pixel_x + dx, pixel_y + dy)
                    pixels.append((r, g, b))
                except (IndexError, KeyError):
                    continue  

        if not pixels:
            return (255, 255, 255)  
        
        avg_color = np.mean(pixels, axis=0).astype(int)
        return tuple(avg_color)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update_idletasks()  

def update_status(message):
    status_bar.config(text=message)
    root.update_idletasks()

def pick_color():
    global is_picking
    update_status("Click anywhere to pick a color...")
    root.update()

    def on_click(x, y, button, pressed):
        global is_picking
        if pressed:
            r, g, b = get_average_color(x, y, size=5)
            color_hex = f'#{r:02x}{g:02x}{b:02x}'

            rgb_label.config(text=f'RGB: {r}, {g}, {b}')
            hex_label.config(text=f'HEX: {color_hex}')
            color_display.config(bg=color_hex)
            update_status("Press 'Pick Color' to select again.")

            listener.stop()  
            root.focus_force()  
            is_picking = False  

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def start_pick_color():
    global is_picking
    if not is_picking:
        is_picking = True
        threading.Thread(target=pick_color, daemon=True).start()

root = tk.Tk()
root.title("Color Picker")
root.geometry("360x200")
root.attributes('-topmost', True)

status_label = tk.Label(root, text="Press 'Pick Color' to start.", font=("Arial", 12))
status_label.pack(pady=5)

display_frame = tk.Frame(root)
display_frame.pack(pady=5, padx=10, fill="x")

color_display = tk.Label(display_frame, text="", width=10, height=5, bg="white", relief="solid", borderwidth=3)
color_display.pack(side="left", padx=5)

text_frame = tk.Frame(display_frame)
text_frame.pack(side="right", expand=True, fill="x")

rgb_frame = tk.Frame(text_frame)
rgb_frame.pack(fill="x", pady=2)
rgb_label = tk.Label(rgb_frame, text="RGB: ?, ?, ?", font=("Arial", 12, "bold"))
rgb_label.pack(side="left", padx=5)
rgb_copy_btn = tk.Button(rgb_frame, text="Copy", command=lambda: copy_to_clipboard(rgb_label.cget("text")[5:]), font=("Arial", 10))
rgb_copy_btn.pack(side="right", padx=5)

hex_frame = tk.Frame(text_frame)
hex_frame.pack(fill="x", pady=2)
hex_label = tk.Label(hex_frame, text="HEX: #??????", font=("Arial", 12, "bold"))
hex_label.pack(side="left", padx=5)
hex_copy_btn = tk.Button(hex_frame, text="Copy", command=lambda: copy_to_clipboard(hex_label.cget("text")[5:]), font=("Arial", 10))
hex_copy_btn.pack(side="right", padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

pick_button = tk.Button(button_frame, text="Pick Color", command=start_pick_color, font=("Arial", 12))
pick_button.pack(side="left", padx=10, pady=5)

credit_label = tk.Label(text_frame, text="@made by kian <3")
credit_label.pack(side="left", padx=5)

exit_button = tk.Button(button_frame, text="Quit", command=exit_app, font=("Helvetica", 12))
exit_button.pack(side="left", padx=10, pady=5)

status_bar = tk.Label(root, text="Waiting for button click...", bd=1, relief="sunken", anchor="w", font=("Arial", 10))
status_bar.pack(side="bottom", fill="x")

root.mainloop()
