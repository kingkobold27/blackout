
#!/usr/bin/env python3

"""Update of last runtime, updated to include: Windows support, Hidden Processes, 
Pictures, Red Team signature, Persistence, remote time change, and terminal effect.

took out fun_facts for sake of space
"""


import os
import signal
import subprocess
import sys
import time
import random
import tkinter as tk

SCRIPT_PATH = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.search_cmd")
DELAY = 20000

FUN_FACTS = ["Gumper_Placeholder"]

def get_font_name():
    try:
        available_fonts = list(tk.font.families())
    except Exception:
        available_fonts = []
    return "Comic Sans MS" if "Comic Sans MS" in available_fonts else "DejaVu Sans"

def launch_overlay():
    while True:
        proc = subprocess.Popen([sys.executable, SCRIPT_PATH, "--child"])
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
        time.sleep(1)

def run_overlay():
    font_name = get_font_name()

    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
        except Exception:
            pass

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
    canvas.pack()

    x = screen_width // 2
    y = screen_height // 2
    text_color = "#7CFC00"
    font_weight = "bold"

    text_item = canvas.create_text(
        x, y,
        text=random.choice(FUN_FACTS),
        fill=text_color,
        font=(font_name, 50, font_weight),
        width=screen_width - 100,
        justify="center"
    )

    def scale_text():
        font_size = 50
        canvas.itemconfig(text_item, font=(font_name, font_size, font_weight))
        bbox = canvas.bbox(text_item)
        while bbox[3] - bbox[1] > screen_height - 100 and font_size > 10:
            font_size -= 2
            canvas.itemconfig(text_item, font=(font_name, font_size, font_weight))
            bbox = canvas.bbox(text_item)

    scale_text()

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    def toggle_overlay():
        # Hide entire overlay
        root.withdraw()
        # Wait 20 seconds (same as text interval), then show new fact
        root.after(DELAY, show_new_fact)

    def show_new_fact():
        # Pick a new fact that is different from the current one
        current_text = canvas.itemcget(text_item, "text")
        new_word = random.choice(FUN_FACTS)
        while new_word == current_text:
            new_word = random.choice(FUN_FACTS)

        canvas.itemconfig(text_item, text=new_word)
        scale_text()
        root.deiconify()
        root.after(DELAY, toggle_overlay)

    root.after(DELAY, toggle_overlay)

    def on_close():
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    if "--child" in sys.argv:
        run_overlay()
    else:
        launch_overlay()
