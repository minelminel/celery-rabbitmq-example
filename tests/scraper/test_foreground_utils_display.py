import pytest

from artifice.scraper.foreground.utils.display import requests_per_minute


def test_app_requests_per_minute():
    # uptime <str>  '0:00:21'
    # hits <int>    21
    uptime = '0:00:21'
    hits = 21
    rpm = requests_per_minute(uptime, hits)
    assert rpm == 21

    uptime = '0:00:00'
    hits = 100
    rpm = requests_per_minute(uptime, hits)
    assert rpm == 100

    uptime = '0:10:00'
    hits = 10
    rpm = requests_per_minute(uptime, hits)
    assert rpm == 1

    uptime = '1:00:00'
    hits = 60
    rpm = requests_per_minute(uptime, hits)
    assert rpm == 1

    uptime = '0:00:00'
    hits = None
    rpm = requests_per_minute(uptime, hits)
    assert rpm == 'unavailable'
