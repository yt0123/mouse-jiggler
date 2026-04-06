#!/usr/bin/env python

import time

import pyautogui


def main():
    # Move mouse slightly every 60 seconds
    try:
        while True:
            # Get current position
            x, y = pyautogui.position()
            # Move slightly to the right
            pyautogui.move(1, 0, duration=0.1)
            # Move back
            pyautogui.move(-1, 0, duration=0.1)
            print(f"Jiggled at {time.strftime('%H:%M:%S')}")
            # Wait 60 seconds
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nJiggler stopped.")


if __name__ == "__main__":
    main()
