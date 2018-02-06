import wtforms
from wtforms import validators, StringField


class RegistrantForm(wtforms.Form):
    name = StringField(
        'name', validators=[validators.Length(min=1),
                            validators.Required()])
    path = StringField(
        'path', validators=[validators.Length(min=1),
                            validators.Required()])
    author = StringField(
        'path', validators=[validators.Length(min=1),
                            validators.Required()])
    command = StringField(
        'path', validators=[validators.Length(min=1),
                            validators.Required()])
