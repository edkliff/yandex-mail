from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from config import DOMAIN_KEY
from wtforms.fields.html5 import DateField

domains = tuple(DOMAIN_KEY.keys())


class AccountCreator(FlaskForm):
    login = StringField('Username', validators=[DataRequired()])
    domain = SelectField('Domain', choices=[(domain,
                                             '@{}'.format(DOMAIN_KEY[domain][0])) for domain in domains])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add User')


class EditUser(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    name = StringField('First Name')
    sname = StringField('Second Name')
    enabled = BooleanField('Enabled')
    # password = PasswordField('New Password for user')
    birth_date = DateField('Birthday Date', description='YYYY-MM-DD', format='%Y-%m-%d')
    sex = SelectField('Gender', choices=[('0', 'N/A'), ('1', 'Male'), ('2', 'Female')])
    hintq = StringField('Secret question')
    hinta = StringField('Answer')
    submit = SubmitField('Edit User')
