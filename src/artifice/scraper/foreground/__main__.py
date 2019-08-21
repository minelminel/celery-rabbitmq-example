import logging

from . import db, Config, configure_logger
from .views import app

configure_logger(Config)

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

# from .views import app, db
# from .cli import get_Configuration, Configure_logger

# Config = get_Configuration()
# Configure_logger(Config)
# logging.info(f'Starting application with Configuration: \n{Config.__dict__}')

# app = create_flask_app(Config)

# if Config.drop_tables:
#     db.drop_all()
#     db.create_all()

# app.run(
#     host=Config.host,
#     port=Config.port,
#     debug=Config.debug,
#     use_reloader=Config.use_reloader,
# )
