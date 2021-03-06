from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     DateField, DecimalField, RadioField)
from wtforms.validators import DataRequired, InputRequired

from app.models import DB


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NAndTwoDatesForm(FlaskForm):
    n = DecimalField(validators=[InputRequired()])
    date1 = DateField(validators=[DataRequired()])
    date2 = DateField(validators=[DataRequired()])
    submit = SubmitField('Show')


class TwoDatesForm(FlaskForm):
    date1 = DateField(validators=[DataRequired()])
    date2 = DateField(validators=[DataRequired()])
    submit = SubmitField('Show')


class ShowButtonForm(FlaskForm):
    submit = SubmitField('Show')


class HumanActionKillForm(FlaskForm):
    alien = StringField('Victim', validators=[DataRequired()])
    submit = SubmitField('Do!')


class HumanActionEscapeForm(FlaskForm):
    submit = SubmitField('Do!')


class AdminLogExcursionsForm(FlaskForm):
    # show all aliens
    alien = StringField('Alien', validators=[DataRequired()])
    # show all humans
    human = StringField('Human', validators=[DataRequired()])
    date1 = DateField(validators=[DataRequired()])
    date2 = DateField(validators=[DataRequired()])
    submit = SubmitField('Show')


class AdminActionAddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Role', choices=[('human', 'human'), ('alien', 'alien')],
                      validators=[DataRequired()])
    submit = SubmitField('Add user')


class AdminActionDestroyShipForm(FlaskForm):
    # show all ships
    ship = StringField('Ship', validators=[DataRequired()])
    submit = SubmitField('Do!')


class AdminActionAddShipForm(FlaskForm):
    # show all alien groups
    alien = StringField('Alien group', validators=[DataRequired()])
    # show all human groups
    human = StringField('Human group', validators=[DataRequired()])

    coordinate = DecimalField(validators=[DataRequired()])
    name = StringField("Star ship name", validators=[DataRequired()])
    submit = SubmitField('Create!')


class AlienActionStealForm(FlaskForm):
    # show all human groups
    human = StringField('Human', validators=[DataRequired()])
    submit = SubmitField('Steal!')


class AlienActionExcursionForm(FlaskForm):
    submit = SubmitField('Do')


class AlienActionExperimentForm(FlaskForm):
    # show all human groups
    human = StringField('Human', validators=[DataRequired()])
    submit = SubmitField('Do')


class AlienActionTransportationForm(FlaskForm):
    # show all ships
    destination = StringField('To ship', validators=[DataRequired()])
    # show all humans from ship
    human = StringField('Human', validators=[DataRequired()])
    submit = SubmitField('Do')