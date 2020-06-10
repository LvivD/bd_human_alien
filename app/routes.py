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
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        print('user in login:', user.username, user.id, user.password_hash,
              user.role)
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
@login_required
def index():
    print("from index:", current_user.is_authenticated)
    if current_user.is_authenticated:
        print(current_user.id, current_user.username,
              current_user.password_hash, current_user.role)

    return redirect(url_for(current_user.role))


@app.route("/home")
@login_required
def home():
    print("from home:", current_user.is_authenticated)
    if current_user.is_authenticated:
        print(current_user.id, current_user.username,
              current_user.password_hash, current_user.role)
    if current_user.is_authenticated:
        return render_template("home.html", user=current_user)
    else:
        return render_template("home.html")


@app.route("/alien")
@login_required
def alien():
    if current_user.role == "human":
        return render_template("human.html")
    return render_template("alien.html", user=current_user)


@app.route("/human")
@login_required
def human():
    if current_user.role == "alien":
        return render_template("alien.html")
    return render_template("human.html", user=current_user)


@app.route("/admin")
@login_required
def admin():
    print('admin page, curr user role:', current_user.role)
    if current_user.role != "admin":
        return redirect(url_for(current_user.role))
    return render_template("admin.html", user=current_user)


@app.route("/admin_actions/add_user", methods=['GET', 'POST'])
@login_required
def add_user():
    form = AdminActionAddUserForm()

    if form.validate_on_submit():
        DB.add_user(username=form.username.data,
                    password_hash=generate_password_hash(form.password.data),
                    role=form.role.data)
        flash('New user was added.')
    return render_template("admin_actions/add_user.html", form=form,
                           user=current_user)


@app.route("/admin_actions/add_ship", methods=['GET', 'POST'])
@login_required
def admin_actions_add_ship():
    form = AdminActionAddShipForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("admin_actions/add_ship.html", form=form,
                           user=current_user)


@app.route("/admin_actions/destroy_ship", methods=['GET', 'POST'])
@login_required
def admin_actions_destroy_ship():
    form = AdminActionDestroyShipForm()
    ships_dict = DB.get_ships_for_crashing()
    if form.validate_on_submit():
        if form.ship.data in ships_dict:
            DB.destroy_ship(form.ship.data)
            flash('Ship was destroyed.')
        flash('Wrong ship name.')
    return render_template("admin_actions/destroy_ship.html", form=form,
                           user=current_user, ships=ships_dict)


@app.route("/admin_log/alien_steals", methods=['GET', 'POST'])
@login_required
def admin_log_alien_steals():
    form = NAndTwoDatesForm()
    res = ''
    if form.validate_on_submit():
        res = DB.aliens_that_theft_more_then_n(form.date1.data, form.date2.data, form.n.data)
    return render_template("adm_logs/alien_steals.html", form=form,
                           user=current_user, res=res)


@app.route("/admin_log/excursions", methods=['GET', 'POST'])
@login_required
def admin_log_excursions():
    form = AdminLogExcursionsForm()
    res = ''
    human_dict = DB.get_all_humans()
    alien_dict = DB.get_all_aliens()
    if form.validate_on_submit():
        res = DB.common_exc_and_exp_for_human_and_alien(
            human_dict[form.human.data],
            alien_dict[form.alien.data],
            form.date1.data,
            form.date2.data)
    return render_template("adm_logs/excursions.html", form=form,
                           user=current_user, res=res, 
                           humans=list(human_dict.keys()),
                           aliens=list(alien_dict.keys()))


@app.route("/admin_log/human_steals", methods=['GET', 'POST'])
@login_required
def admin_log_human_steals():
    form = NAndTwoDatesForm()
    res = ''
    if form.validate_on_submit():
        res = DB.were_thefted_more_then_n_times(form.date1.data, form.date2.data, form.n.data)
    return render_template("adm_logs/human_steals.html", form=form,
                           user=current_user, res=res)


@app.route("/admin_log/ships", methods=['GET', 'POST'])
@login_required
def admin_log_ships():
    form = ShowButtonForm()
    res = []
    if form.validate_on_submit():
        res = DB.get_ships_for_crashing()

    return render_template("adm_logs/ships.html", form=form, user=current_user, res=res)


@app.route("/admin_log/total_steals", methods=['GET', 'POST'])
@login_required
def admin_log_total_steals():
    form = ShowButtonForm()
    res = []
    if form.validate_on_submit():
        res = DB.thefts_by_month()
    return render_template("adm_logs/total_steals.html", form=form,
                           user=current_user, res=res)


@app.route("/human_actions/escape", methods=['GET', 'POST'])
@login_required
def human_actions_escape():
    form = HumanActionEscapeForm()
    if form.validate_on_submit():
        DB.escape_from_ship(current_user.id)
        flash('You escaped.')
        return redirect(url_for(current_user.role))
    return render_template("human_actions/escape.html", form=form,
                           user=current_user)


@app.route("/human_actions/kill", methods=['GET', 'POST'])
@login_required
def human_actions_kill():
    form = HumanActionKillForm()
    aliens_on_ship = DB.get_info_by_user(current_user.id)[2]

    if form.validate_on_submit():
        if form.alien.data in list(aliens_on_ship.keys()):
            res = DB.human_kill_alien(current_user.id,
                                      aliens_on_ship[form.alien.data])
            if res:
                flash('Alien was killed')
                return redirect(url_for("index"))
            flash("Something wrong. Alien wasn't killed")

        else:
            flash("Wrong alien name. Alien wasn't killed")

    return render_template("human_actions/kill.html", form=form,
                           user=current_user,
                           aliens_on_ship=list(aliens_on_ship.keys()))


@app.route("/human_logs/kill", methods=['GET', 'POST'])
@login_required
def human_logs_kill():
    form = TwoDatesForm()
    res=""
    if form.validate_on_submit():
        res = DB.killed_by_me(current_user.id, form.date1.data, form.date2.data)
    return render_template("human_logs/kill.html", form=form,
                           user=current_user, res=res)


@app.route("/human_logs/ships", methods=['GET', 'POST'])
@login_required
def human_logs_ships():
    form = TwoDatesForm()
    ships = ""
    if form.validate_on_submit():
        ships = DB.ships_visited(current_user.id, form.date1.data, form.date2.data)[2:]
    return render_template("human_logs/ships.html", form=form, user=current_user, ships=ships)


@app.route("/human_logs/steal", methods=['GET', 'POST'])
@login_required
def human_logs_steal():
    form = NAndTwoDatesForm()
    res = ""
    if form.validate_on_submit():
        res = DB.get_all_who_theft_me_more_then_n(current_user.id, form.date1.data, form.date2.data, form.n.data)
        print(res)
    return render_template("human_logs/steal.html", form=form,
                           user=current_user, res=res)


@app.route("/human_logs/steal_and_kill", methods=['GET', 'POST'])
@login_required
def human_logs_steal_and_kill():
    form = ShowButtonForm()
    res = ""
    if form.validate_on_submit():
        res = DB.theft_and_killed_by_me(current_user.id)
        print(res)
    return render_template("human_logs/steal_and_kill.html", form=form,
                           user=current_user, res=res)


@app.route("/human_logs/experiment", methods=['GET', 'POST'])
@login_required
def human_logs_experiment():
    form = NAndTwoDatesForm()
    res = ""
    if form.validate_on_submit():
        res = DB.experimented_by_n(current_user.id, form.date1.data, form.date2.data, form.n.data)
    return render_template("human_logs/experiment.html", form=form,
                           user=current_user, res=res)


@app.route("/alien_actions/steal", methods=['GET', 'POST'])
@login_required
def alien_actions_steal():
    form = AlienActionStealForm()
    if form.validate_on_submit():
        DB.alien_take_human_to_ship(current_user.id, form)
        flash('Stolen.')
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
    if form.validate_on_submit():
        # DB.alien_take_human_to_ship(current_user.id, form)
        DB.make_excursion(current_user.id, form)
        flash('Excursion done')
    return render_template("alien_actions/excursion.html", form=form,
                           user=current_user)


@app.route("/alien_actions/experiment", methods=['GET', 'POST'])
@login_required
def alien_actions_experiment():
    form = AlienActionExperimentForm()
    if form.validate_on_submit():
        # DB.alien_take_human_to_ship(current_user.id, form)
        DB.make_experiment(current_user.id, form)
        flash('Experiment done')
    return render_template("alien_actions/experiment.html", form=form,
                           user=current_user)


@app.route("/alien_logs/excursion", methods=['GET', 'POST'])
@login_required
def alien_logs_experiment():
    form = NAndTwoDatesForm()
    res = ''
    if form.validate_on_submit():
        res = DB.excursions_by_alien_with_more_then_n(current_user.id, form.date1.data, form.date2.data, form.n.data)
    return render_template("alien_logs/excursion.html", form=form,
                           user=current_user, res=res)


@app.route("/alien_logs/steal", methods=['GET', 'POST'])
@login_required
def alien_logs_steal():
    form = NAndTwoDatesForm()
    # if form.validate_on_submit():
    # flash('New user was added.')
    return render_template("alien_logs/steal.html", form=form,
                           user=current_user)
