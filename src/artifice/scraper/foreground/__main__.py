import logging

from .views import app, db
from .config import get_configuration, configure_logger

config = get_configuration()
configure_logger(config)
logging.info(f'Starting application with configuration: \n{config.__dict__}')

# app = create_flask_app(config)

if config.drop_tables:
    db.drop_all()
    db.create_all()

app.run(
    host=config.host,
    port=config.port,
    debug=config.debug,
    use_reloader=config.use_reloader,
)






# import os
# import logging
#
# from .views import app, db
#
# db.drop_all()
# db.create_all()
# app.run(
#     host='0.0.0.0',
#     port=8080,
#     debug=True,
#     use_reloader=True,
# )
