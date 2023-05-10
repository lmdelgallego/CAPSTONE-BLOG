from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        label="Email",
        validators=[
            DataRequired(),
            Email(message="That's not a valid email address"),
            Length(min=6, message="Litter short for an email address?"),
        ],
    )
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log in")
