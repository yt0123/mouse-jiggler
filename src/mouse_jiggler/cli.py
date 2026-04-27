import asyncio
import logging
import time

import click
from rich.console import Console

from mouse_jiggler.core import MouseJiggler

console = Console()


@click.command()
@click.option("-t", "--time-interval", default=60.0, help="Time interval in seconds between each jiggle.")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode to print detailed information about each jiggle.")
def jiggle(time_interval: float, debug: bool):
    """
    Jiggle the mouse cursor at regular intervals to prevent the computer
    from going to sleep or activating a screensaver.
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    jiggler = MouseJiggler(time_interval)

    async def run_forever():
        background_task = asyncio.create_task(jiggler.start())
        try:
            if debug:
                # In debug mode, run indefinitely without a status spinner.
                await asyncio.Future()
            else:
                with console.status(
                        f"[bold green]Jiggling the mouse every {time_interval:.1f} seconds... (Press Ctrl+C to stop)",
                        spinner="dots"):
                    await asyncio.Future()
        except asyncio.CancelledError:
            jiggler.stop()
            await background_task

    try:
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    jiggle()
