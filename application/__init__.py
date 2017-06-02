from flask import Flask
from application.database import init_db
from application.service import Service


app = Flask(__name__)
app.config.from_object('application.config')
session = init_db(app.config)
service = Service(session)
