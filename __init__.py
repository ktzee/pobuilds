from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

from home import views
from builds import views
