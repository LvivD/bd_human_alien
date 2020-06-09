from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     DateField, DecimalField, RadioField, )
from wtforms.validators import DataRequired


from app.models import DB

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NAndTwoDatesForm(FlaskForm):
    n = DecimalField(validators=[DataRequired()])
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
    # def __init__(self, id):
    #     super().__init__()
    #     self._id = id
    #     aliens_list = DB.get_all_aliens_on_the_ship(self._id)
    #     self.aliens_list = [(alien, alien) for alien in aliens_list]
    #     self.alien = RadioField('Aliens', choices=aliens_list)

    # aliens_list = []
    # alien = RadioField('Aliens', choices=aliens_list)
    alien = StringField('Victim', validators=[DataRequired()])
    submit = SubmitField('Do!')

    # def choose_human(self, id):
    #     self.aliens_list = DB.get_all_aliens_on_the_ship(id)
    #     self.aliens_list = [(alien, alien) for alien in self.aliens_list]
    #     self.alien = RadioField('Aliens', choices=self.aliens_list)

class HumanActionEscapeForm(FlaskForm):
    submit = SubmitField('Do!')


class AdminLogExcursionsForm(FlaskForm):
    alien = RadioField()
    human = RadioField()
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
    ship = RadioField()
    submit = SubmitField('Do!')


class AdminActionAddShipForm(FlaskForm):
    aliens_group = RadioField()
    human_group = RadioField()
    coordinate = DecimalField(validators=[DataRequired()])
    name = StringField("Star ship name", validators=[DataRequired()])
    submit = SubmitField('Create!')


class AlienActionStealForm(FlaskForm):
    human = RadioField()
    submit = SubmitField('Steal!')


class AlienActionExcursionForm(FlaskForm):
    submit = SubmitField('Do')


class AlienActionExperimentForm(FlaskForm):
    human = RadioField()
    submit = SubmitField('Do')


class AlienActionTransportationForm(FlaskForm):
    departure = RadioField()
    destination = RadioField()
    whom = RadioField()
    submit = SubmitField('Do')


class AlienLogsExperimentForm(FlaskForm):
    human = RadioField()
    submit = SubmitField('Do')


class AlienLogsStealForm(FlaskForm):
    human = RadioField()
    submit = SubmitField('Do')
