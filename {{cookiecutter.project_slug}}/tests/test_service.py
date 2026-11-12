from __future__ import annotations

import threading

from {{ cookiecutter.package_name }} import service


def test_run_stops_when_event_set() -> None:
    stop = threading.Event()
    stop.set()  # already requested to stop
    service.run(stop, interval=0.01)  # returns immediately, no hang


def test_run_handles_polled_items(monkeypatch) -> None:
    handled: list[object] = []
    stop = threading.Event()

    def fake_handle(item: object) -> None:
        handled.append(item)
        stop.set()  # stop after the first batch

    monkeypatch.setattr(service, "poll_once", lambda: ["a", "b"])
    monkeypatch.setattr(service, "handle", fake_handle)

    service.run(stop, interval=0.01)
    assert handled == ["a", "b"]


def test_poll_once_default_empty() -> None:
    assert service.poll_once() == []
