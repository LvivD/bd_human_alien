from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
from app.models import DB

DB.connect()
from app import routes







