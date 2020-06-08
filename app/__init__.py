from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)

from app import routes





