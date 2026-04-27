import asyncio
import logging
import platform
import threading
import time

import pyautogui

if platform.system() == "Darwin":
    import AppKit

    # Run the script in the background on macOS
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSBackgroundOnly"] = "1"


class MouseJiggler:
    """
    A jiggler that runs in the background cooperatively with the event loop and moves the mouse cursor slightly
    at regular intervals to prevent the computer from going to sleep or activating a screensaver.
    """

    def __init__(self, time_interval: float):
        """
        :param time_interval: The time in seconds to wait between each jiggle. Must be a positive number.
        """
        self.__last_jiggled_at = 0.0
        self.__time_interval = time_interval
        self.__stop_event = asyncio.Event()
        self.__logger = logging.getLogger(__name__)

    def get_last_jiggled_at(self) -> float:
        """
        Get the timestamp of the last jiggle.
        :return: The timestamp of the last jiggle in seconds since the epoch. 0.0 if never jiggled.
        """
        return self.__last_jiggled_at

    def stop(self):
        """
        Stop the jiggler.
        """
        self.__stop_event.set()

    async def start(self):
        """
        Start the jiggler asynchronously.
        """
        self.__logger.debug("Starting up jiggler with time interval: %.2f seconds",
                            self.__time_interval)
        while not self.__stop_event.is_set():
            self.__jiggle()
            try:
                await asyncio.wait_for(self.__stop_event.wait(), timeout=self.__time_interval)  # Cooperative sleep
            except asyncio.TimeoutError:
                # No stop signal received, so jiggle again.
                continue
        self.__logger.debug("Wrapped up jiggler")

    def __jiggle(self):
        """
        Jiggle the mouse cursor.
        """
        # Get current position
        x, y = pyautogui.position()
        self.__logger.debug("Current mouse position: (%d, %d)", x, y)
        # Move slightly to the right
        pyautogui.move(1, 0, duration=0.1)
        # Move back
        pyautogui.move(-1, 0, duration=0.1)
        self.__last_jiggled_at = time.time()
        self.__logger.debug("Jiggled at %s", time.ctime(self.__last_jiggled_at))
