import logging

from . import db, Config, configure_logger
from .routes import app

configure_logger(Config)
logging.info(f'Starting application with Configuration: \n{Config.__dict__}')

# app = create_app()
if Config.DROP_TABLES:
    db.drop_all()
    db.create_all()

app.run(
    host=Config.FLASK_HOST,
    port=Config.FLASK_PORT,
    debug=Config.FLASK_DEBUG,
    use_reloader=Config.FLASK_USE_RELOADER,
)
