from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    email = StringField(
        label="Email",
        validators=[
            DataRequired(),
            Email(message="That's not a valid email address"),
            Length(min=6, message="Litter short for an email address?"),
        ],
    )
    password = PasswordField(label="Password", validators=[DataRequired()])
    name = StringField(label="Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")
