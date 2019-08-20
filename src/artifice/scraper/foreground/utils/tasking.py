from artifice.scraper.background import holding_tank

def send_to_celery(url, **kwargs):
    task = holding_tank.delay(url, **kwargs)
    return task
