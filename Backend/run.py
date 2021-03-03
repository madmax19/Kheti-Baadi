import os
from app import app, db
from routes import *
from models import *


@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()


app.run(debug=True, host='127.0.0.1', port=8000)
