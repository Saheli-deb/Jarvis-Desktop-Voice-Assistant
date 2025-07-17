# scroll_control.py

import pyautogui

def scroll_up(units=10):
    """Scrolls up the screen by the given number of units."""
    try:
        pyautogui.scroll(100 * units)
        print(f"[↑] Scrolled up {units} units.")
    except Exception as e:
        print(f"[✖] Error scrolling up: {e}")

def scroll_down(units=10):
    """Scrolls down the screen by the given number of units."""
    try:
        pyautogui.scroll(-100 * units)
        print(f"[↓] Scrolled down {units} units.")
    except Exception as e:
        print(f"[✖] Error scrolling down: {e}")
