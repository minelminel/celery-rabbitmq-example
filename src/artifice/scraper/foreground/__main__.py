import logging
from pprint import pformat

from artifice import artifice_logo
from artifice.scraper.config.logger import configure_logger
from artifice.scraper.foreground import settings
from . import create_app

configure_logger(settings)
logging.info(artifice_logo())
logging.info(f'Starting application with Configuration: \n{pformat(settings.__dict__)}\n')

application = create_app()

application.run(
    host=settings.FLASK_HOST,
    port=settings.FLASK_PORT,
    debug=settings.FLASK_DEBUG,
    use_reloader=settings.FLASK_USE_RELOADER,
)
