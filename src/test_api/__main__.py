# import os
#
# from . import app as application
# from . import db as database
#
#
# # try:
# #     os.mkdir(application.config.get('DB_TEMP_DIR'))
# # except FileExistsError:
# #     pass
# # finally:
# #     database.create_all()
#
#
# application.run(
#     port=application.config.get('FLASK_PORT'),
#     host=application.config.get('FLASK_HOST'),
#     debug=application.config.get('FLASK_DEBUG'),
#     use_reloader=application.config.get('FLASK_USE_RELOADER'),
# )
