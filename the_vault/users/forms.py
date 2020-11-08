"""Import libraries."""
from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
    EqualTo,
)
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
)
from the_vault.models import User


class RegistrationForm(FlaskForm):
    """User registration form."""

    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        """Validate email is not in use."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                """
                The email is already in use. Please enter a different email.
                Alternatively, if you forgot your password, go to the signin
                page and click \"Forgot Password\".
                """
            )


class LoginForm(FlaskForm):
    """User signin form."""

    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class UpdateAccountForm(FlaskForm):
    """User update account form."""

    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_email(self, email):
        """Validate email is not in use."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                """
                    The email is already in use. Please enter a different email.
                    Alternatively, if you forgot your password, go to the signin
                    page and click \"Forgot Password\".
                    """
            )
