from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        print("if user exist:", user.if_exists())
        print(user.authenticate(form.password.data))
        if not user.if_exists() or not user.authenticate(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def home():
    try:
        print(current_user.id)
    except Exception:
        pass
    return render_template("home.html")

@app.route("/alien")
def alien():
    try:
        print(current_user.id)
    except Exception:
        pass
    return render_template("alien.html")

@app.route("/human")
def human():
    try:
        print(current_user.id)
    except Exception:
        pass
    return render_template("human.html")
