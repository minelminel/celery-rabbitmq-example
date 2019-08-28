import pytest


def test_background_util_report_ready():
    from artifice.scraper.background.util import report_ready
    url = 'https://www.google.com'
    report = report_ready(url)
    assert report['url'] == url
    assert report['status'] == 'READY'

def test_background_util_report_done():
    from artifice.scraper.background.util import report_done
    url = 'https://www.google.com'
    report = report_done(url)
    assert report['url'] == url
    assert report['status'] == 'DONE'
