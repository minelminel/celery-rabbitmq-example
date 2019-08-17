import os

from .views import app, db

db.drop_all()
db.create_all()
app.run(
    host='0.0.0.0',
    port=8080,
    debug=True,
    use_reloader=False,
)
