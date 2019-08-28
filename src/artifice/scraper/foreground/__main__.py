import logging

from artifice.scraper.config.logger import configure_logger
import artifice.scraper.config.settings as settings
from . import create_app


configure_logger(settings)
logging.info(f'Starting application with Configuration: \n{settings.__dict__}')

app = create_app()

app.run(
    host=settings.FLASK_HOST,
    port=settings.FLASK_PORT,
    debug=settings.FLASK_DEBUG,
    use_reloader=settings.FLASK_USE_RELOADER,
)
