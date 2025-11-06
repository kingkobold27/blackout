#!/usr/bin/env python3
import os
import sys
import tkinter as tk
import signal

# File to track command count
count_file = os.path.expanduser("~/.dottracker_count")
os.makedirs(os.path.dirname(count_file), exist_ok=True)

# Read/update count
if os.path.exists(count_file):
    with open(count_file, "r") as f:
        count = int(f.read().strip())
else:
    count = 0
count += 1
with open(count_file, "w") as f:
    f.write(str(count))

# Calculate dot size
radius = 10 + int(count ** 0.5 * 5)

# Kill previous overlay if PID file exists
pid_file = os.path.expanduser("~/.dottracker_overlay_pid")
if os.path.exists(pid_file):
    try:
        with open(pid_file, "r") as f:
            old_pid = int(f.read().strip())
        os.kill(old_pid, signal.SIGTERM)
    except:
        pass

# Write current PID
with open(pid_file, "w") as f:
    f.write(str(os.getpid()))

# Fullscreen opaque overlay
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                   bg="black", highlightthickness=0)
canvas.pack()

# Draw dot in center
x = root.winfo_screenwidth() // 2
y = root.winfo_screenheight() // 2
canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="black")

root.mainloop()
