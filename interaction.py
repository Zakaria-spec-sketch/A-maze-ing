import os
import sys
import random

# Windows
if os.name == "nt":
    import msvcrt
else:
    import tty
    import termios


def get_key():
    if os.name == "nt":
        return msvcrt.getch().decode("utf-8").lower()
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch.lower()


def clear():
    os.system("cls" if os.name == "nt" else "clear")
