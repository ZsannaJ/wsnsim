import pytest

from sim.scheduler import Scheduler

def test_chronological_order():
    """Ellenőrzi, hogy az események időrendben futnak-e le."""
    res = []
    s = Scheduler()
    s.schedule(1.5, lambda _: res.append("második"))
    s.schedule(0.5, lambda _: res.append("első"))
    s.run(until=2.0)
    assert res == ["első", "második"]

def test_priority_tie_breaker():
    """Azonos időpontnál a prioritás dönt (kisebb érték = nagyobb prioritás)."""
    res = []
    s = Scheduler()
    s.schedule(1.0, lambda _: res.append("alacsony"), priority=10)
    s.schedule(1.0, lambda _: res.append("magas"), priority=1)
    s.run(until=2.0)
    assert res == ["magas", "alacsony"]

def test_reproducibility():
    """Ellenőrzi, hogy a szimulált idő pontosan követi az eseményeket."""
    s = Scheduler()
    s.schedule(0.123, lambda _: None)
    s.run(until=0.5)
    assert s.current_time == 0.123