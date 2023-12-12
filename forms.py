""" Forms for our notes app. """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class CreateUserForm(FlaskForm):
    """ Forms to create a user. """

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=6, max=30)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=30)]
    )

    email = EmailField(
        "Email address",
        validators=[InputRequired()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=1, max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=1, max=30)]
    )


class LoginUserForm(FlaskForm):
    """ Form to log in user"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )


