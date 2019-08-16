import os

from .views import app, db




# def reset_database():
#     DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'site.db')
#     os.remove(DB_FILE)
#
# reset_database()
db.drop_all()
db.create_all()
app.run(
    host='0.0.0.0',
    port=8080,
    debug=True,
    use_reloader=True,
)
