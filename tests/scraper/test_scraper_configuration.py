# try to import the file from an environment variable
import os

def test_artifice_scraper_settings_located():
    # try to get environment settings
    settings = os.environ.get('ARTIFICE_SCRAPER_SETTINGS', None)
    source = 'ENV'
    if not settings:
        from artifice.scraper.foreground import settings
        source = 'AUTO'
    assert source is 'ENV' or 'AUTO'
    assert settings
