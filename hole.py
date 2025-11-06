#!/usr/bin/env python3
import os
import signal
import subprocess

# -------------------------------
# Ensure tkinter is installed via apt
# -------------------------------
try:
    import tkinter as tk
except ImportError:
    print("tkinter not found, attempting to install via apt...")
    try:
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3-tk"])
        import tkinter as tk
    except Exception:
        print("Failed to install tkinter. Please install manually with:")
        print("sudo apt install python3-tk")
        exit(1)

# -------------------------------
# Files to track command count and overlay PID
# -------------------------------
count_file = os.path.expanduser("~/.dottracker_count")
pid_file = os.path.expanduser("~/.dottracker_overlay_pid")
os.makedirs(os.path.dirname(count_file), exist_ok=True)

# -------------------------------
# Function to show overlay
# -------------------------------
def show_overlay():
    # Update count
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

    # Kill previous overlay if exists
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
        except:
            pass

    # Fullscreen overlay
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                       height=root.winfo_screenheight(),
                       bg="black", highlightthickness=0)
    canvas.pack()

    # Draw dot in center
    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="black")

    # Save PID
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

    # Close after 10 seconds and restart
    def restart():
        root.destroy()
        os.system("clear")  # clear terminal at the end of each overlay
        show_overlay()       # call again

    root.after(10000, restart)  # overlay visible for 10 seconds
    root.mainloop()

# -------------------------------
# Start looping overlay
# -------------------------------
show_overlay()
