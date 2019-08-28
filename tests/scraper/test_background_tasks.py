import pytest

url = 'https://www.npr.org/sections/politics'

def test_backend_tasks_sorting_hat_needs_host():
    from artifice.scraper.background.tasks import sorting_hat
    with pytest.raises(ConnectionError):
        sorting_hat(url)
