from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from config import DOMAIN_KEY

domains = tuple(DOMAIN_KEY.keys())


class MailCreator(FlaskForm):
    login = StringField('Username', validators=[DataRequired()])
    domain = SelectField('Domain', choices=[(domain,
                                             '@{}'.format(DOMAIN_KEY[domain][0])) for domain in domains])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add User')
