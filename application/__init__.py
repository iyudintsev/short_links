import os
from flask import Flask
from application.database import init_db
from application.service import Service


def remove_db():
    path = 'sqlite.db'
    if os.path.exists(path):
        os.remove(path)


app = Flask(__name__)
app.config.from_object('application.config')

remove_db()

session = init_db(app.config)
service = Service(session)
