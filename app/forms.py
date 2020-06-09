from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     DateField, DecimalField, RadioField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class HumanLogStealForm(FlaskForm):
    date1 = DateField(validators=[DataRequired])
    date2 = DateField(validators=[DataRequired])
    n = DecimalField(validators=[DataRequired])
    submit = SubmitField('Show')


class HumanLogKillForm(FlaskForm):
    date1 = DateField(validators=[DataRequired])
    date2 = DateField(validators=[DataRequired])
    submit = SubmitField('Show')


class HumanLogShipsForm(FlaskForm):
    date1 = DateField(validators=[DataRequired])
    date2 = DateField(validators=[DataRequired])
    submit = SubmitField('Show')


class HumanLogStealAndKillForm(FlaskForm):
    submit = SubmitField('Show')


class HumanLogExperimentForm(FlaskForm):
    n = DecimalField(validators=[DataRequired])
    date1 = DateField(validators=[DataRequired])
    date2 = DateField(validators=[DataRequired])
    submit = SubmitField('Show')


class AdminLogAlienStealsForm(FlaskForm):
    n = DecimalField(validators=[DataRequired])
    date1 = DateField(validators=[DataRequired])
    date2 = DateField(validators=[DataRequired])
    submit = SubmitField('Show')


class AdminLogHumanStealsForm(FlaskForm):
    n = DecimalField(validators=[DataRequired()])
    date1 = DateField(validators=[DataRequired()])
    date2 = DateField(validators=[DataRequired()])
    submit = SubmitField('Show')


class AdminLogExcursionsForm(FlaskForm):
    alien = RadioField()
    human = RadioField()
    date1 = DateField(validators=[DataRequired])
    date2 = DateField(validators=[DataRequired])
    submit = SubmitField('Show')


class AdminLogTotalStealsForm(FlaskForm):
    submit = SubmitField('Show')


class HumanActionKillForm(FlaskForm):
    alien = RadioField()
    submit = SubmitField('Do!')


class HumanActionEscapeForm(FlaskForm):
    submit = SubmitField('Do!')


class AdminActionAddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField()
    submit = SubmitField('Add user')


class AdminActionDestroyShipForm(FlaskForm):
    role = RadioField()
    submit = SubmitField('Do!')
