from flask import Flask, redirect, url_for, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
import os

app = Flask(__name__)
sockIO = SocketIO(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


import routes, models


if __name__ == '__main__':
    sockIO.run(host="192.168.1.10")
