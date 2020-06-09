from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, DB
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash


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

        # next page handling
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
    print("from home:", current_user.is_authenticated)
    if current_user.is_authenticated:
        print(current_user.id, current_user.username,
              current_user.password_hash)
    return render_template("home.html")


@app.route("/alien")
@login_required
def alien():
    return render_template("alien.html")


@app.route("/human")
@login_required
def human():
    return render_template("human.html")


@app.route("/admin_actions/add_user", methods=['GET', 'POST'])
@login_required
def add_user():
    form = AdminActionAddUserForm()

    if form.validate_on_submit():
        DB.add_user(username=form.username.data, password_hash=generate_password_hash(form.password.data),role=form.role.data)
        flash('New user was added.')
    return render_template("admin_actions/add_user.html", form=form)


@app.route("/admin_actions/add_ship", methods=['GET', 'POST'])
@login_required
def admin_actions_add_ship():
    form = AdminActionAddShipForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("admin_actions/add_ship.html", form=form)


@app.route("/admin_actions/destroy_ship", methods=['GET', 'POST'])
@login_required
def admin_actions_destroy_ship():
    form = AdminActionDestroyShipForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("admin_actions/destroy_ship.html", form=form)


@app.route("/admin_log/alien_steals", methods=['GET', 'POST'])
@login_required
def admin_log_alien_steals():
    form = NAndTwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("adm_logs/alien_steals.html", form=form)


@app.route("/admin_log/excursions", methods=['GET', 'POST'])
@login_required
def admin_log_excursions():
    form = AdminLogExcursionsForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("adm_logs/excursions.html", form=form)


@app.route("/admin_log/human_steals", methods=['GET', 'POST'])
@login_required
def admin_log_human_steals():
    form = NAndTwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("adm_logs/human_steals.html", form=form)


@app.route("/admin_log/ships", methods=['GET', 'POST'])
@login_required
def admin_log_ships():
    form = ShowButtonForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("adm_logs/ships.html", form=form)


@app.route("/admin_log/total_steals", methods=['GET', 'POST'])
@login_required
def admin_log_total_steals():
    form = ShowButtonForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("adm_logs/total_steals.html", form=form)


@app.route("/human_actions/escape", methods=['GET', 'POST'])
@login_required
def human_actions_escape():
    form = HumanActionEscapeForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_actions/escape.html", form=form)


@app.route("/human_actions/kill", methods=['GET', 'POST'])
@login_required
def human_actions_kill():
    form = HumanActionKillForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_actions/kill.html", form=form,
                           user=current_user)


@app.route("/human_logs/kill", methods=['GET', 'POST'])
@login_required
def human_logs_kill():
    form = TwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_logs/kill.html", form=form,
                           user=current_user)


@app.route("/human_logs/ships", methods=['GET', 'POST'])
@login_required
def human_logs_ships():
    form = TwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_logs/ships.html", form=form,
                           user=current_user)


@app.route("/human_logs/steal", methods=['GET', 'POST'])
@login_required
def human_logs_steal():
    form = NAndTwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_logs/steal.html", form=form,
                           user=current_user)


@app.route("/human_logs/steal_and_kill", methods=['GET', 'POST'])
@login_required
def human_logs_steal_and_kill():
    form = ShowButtonForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_logs/steal_and_kill.html", form=form,
                           user=current_user)


@app.route("/human_logs/experiment", methods=['GET', 'POST'])
@login_required
def human_logs_experiment():
    form = NAndTwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("human_logs/experiment.html", form=form,
                           user=current_user)


@app.route("/alien_actions/steal", methods=['GET', 'POST'])
@login_required
def alien_actions_steal():
    form = AlienActionStealForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("alien_actions/steal.html", form=form,
                           user=current_user)


@app.route("/alien_actions/transportation", methods=['GET', 'POST'])
@login_required
def alien_actions_transportation():
    form = AlienActionTransportationForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("alien_actions/transportation.html", form=form,
                           user=current_user)


@app.route("/alien_actions/excursion", methods=['GET', 'POST'])
@login_required
def alien_actions_excursion():
    form = AlienActionExcursionForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("alien_actions/excursion.html", form=form,
                           user=current_user)
