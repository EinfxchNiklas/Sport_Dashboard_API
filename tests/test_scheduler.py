from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

import app.schedulers.scheduler as scheduler_module
from app.schedulers.scheduler import (
    get_scheduler,
    schedule_match_monitor,
    shutdown_scheduler,
)

BERLIN = ZoneInfo("Europe/Berlin")


@pytest.fixture(autouse=True)
def reset_scheduler():
    """Ensure a clean scheduler singleton before and after each test."""
    # Reset singleton before test
    scheduler_module._scheduler = None
    yield
    # Tear down after test
    s = scheduler_module._scheduler
    if s is not None and s.running:
        s.shutdown(wait=False)
    scheduler_module._scheduler = None


def test_get_scheduler_returns_singleton():
    s1 = get_scheduler()
    s2 = get_scheduler()
    assert s1 is s2


def test_scheduler_timezone_berlin():
    s = get_scheduler()
    tz = s.timezone
    # APScheduler stores timezone as a tzinfo-like object; check its zone key
    tz_key = getattr(tz, "key", None) or getattr(tz, "zone", None) or str(tz)
    assert "Europe/Berlin" in tz_key


def test_schedule_match_monitor_adds_job():
    kickoff = datetime(2026, 8, 1, 18, 0, 0, tzinfo=BERLIN)
    job_id = schedule_match_monitor(match_id=1, kickoff_time=kickoff)

    assert job_id == "match-1"
    job = get_scheduler().get_job("match-1")
    assert job is not None
    assert job.id == "match-1"


def test_schedule_match_monitor_replaces_existing_job():
    s = get_scheduler()
    s.start()
    try:
        kickoff = datetime(2026, 8, 1, 18, 0, 0, tzinfo=BERLIN)
        schedule_match_monitor(match_id=1, kickoff_time=kickoff)
        schedule_match_monitor(match_id=1, kickoff_time=kickoff, duration_minutes=120)

        jobs = [j for j in s.get_jobs() if j.id == "match-1"]
        assert len(jobs) == 1
    finally:
        s.shutdown(wait=False)
