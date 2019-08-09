# import os
#
# loc = os.path.dirname(os.path.abspath(__file__))
#
# class Configuration:
#     # paths
#     LOC = loc
#     DB_TEMP_DIR = os.path.join(loc, 'temp')
#     # flask
#     FLASK_PORT = 8080
#     FLASK_HOST ='0.0.0.0'
#     FLASK_DEBUG = True
#     FLASK_USE_RELOADER = True
#     # sqlalchemy
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_DATABASE_URI = os.path.join('sqlite://', loc, 'temp', 'temp.db')
