from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, DB         # DB delete
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash # delete

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        if not user.if_exists() or not user.authenticate(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        #next page handling
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
@login_required
def home():
    print("from home:",current_user.is_authenticated)
    if current_user.is_authenticated:
        print(current_user.id, current_user.username, current_user.password_hash)
    return render_template("home.html")

@app.route("/alien")
@login_required
def alien():
    return render_template("alien.html")

@app.route("/human")
@login_required
def human():
    return render_template("human.html")
