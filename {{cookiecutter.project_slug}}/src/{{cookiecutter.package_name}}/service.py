"""Long-running poller skeleton with graceful shutdown.

Replace `poll_once` and `handle` with real work (e.g. fetch + process email).
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import threading
from importlib.metadata import version

log = logging.getLogger("{{ cookiecutter.package_name }}")


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def poll_once() -> list[object]:
    """Fetch pending items. Return an empty list when there is nothing to do."""
    return []


def handle(item: object) -> None:
    """Process a single item."""
    log.info("handling %r", item)


def run(stop: threading.Event, interval: float) -> None:
    """Poll-handle-sleep loop that exits cleanly when `stop` is set."""
    log.info("started (interval=%ss)", interval)
    while not stop.is_set():
        for item in poll_once():
            handle(item)
        stop.wait(interval)
    log.info("stopped")


def main() -> None:
    parser = argparse.ArgumentParser(description="{{ cookiecutter.description }}")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit.")
    parser.add_argument(
        "--version",
        action="version",
        version=version("{{ cookiecutter.project_slug }}"),
    )
    args = parser.parse_args()

    setup_logging(os.getenv("LOG_LEVEL", "INFO"))
    interval = float(os.getenv("POLL_INTERVAL", "60"))

    stop = threading.Event()
    if args.once:
        for item in poll_once():
            handle(item)
        return

    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    run(stop, interval)
