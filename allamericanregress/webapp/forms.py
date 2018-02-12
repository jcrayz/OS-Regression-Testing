import flask_wtf
from wtforms import validators, StringField


class RegistrantForm(flask_wtf.FlaskForm):
    name = StringField(
        'Registrant Name',
        validators=[validators.Length(min=1),
                    validators.Required()])
    path = StringField(
        'Path to executable',
        validators=[validators.Length(min=1),
                    validators.Required()])
    author = StringField(
        'Program Author',
        validators=[validators.Length(min=1),
                    validators.Required()])
    command = StringField(
        'Shell command',
        validators=[validators.Length(min=1),
                    validators.Required()])
