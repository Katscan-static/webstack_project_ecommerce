from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    """Form for user registration."""

    def validate_username(self, username_check):
        """Validate if username already exists."""
        user = User.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_check):
        """Validate if email address already exists."""
        email = User.query.filter_by(email=email_address_check.data).first()
        if email:
            raise ValidationError('Email address already exists')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    """Form for purchasing an item."""
    
    submit = SubmitField(label='Purchase Item!')


class SellingForm(FlaskForm):
    """Form for selling an item."""

    submit = SubmitField(label="Sell Item!")

