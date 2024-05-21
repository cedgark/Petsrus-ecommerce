from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from wtforms import PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, ValidationError, Regexp,InputRequired
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15,message='Username should be between 3 and 15 characters long.')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=15)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,8}$',message='Your password should be between 6 and 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Regexp('^.{6,8}$',message='Your password should be between 6 and 8 characters.'), EqualTo('password',message='Confirm password not equal to password.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #Allow unique usernames and emails only
        if user:
            raise ValidationError('Username already exist. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address is already associated with another account. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,8}$',message='Your password should be between 6 and 8 characters.')])
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post comment')

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email')
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=300)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    card_number = StringField('Card Number', validators=[DataRequired(), Regexp('^[0-9]{16}$',message='Your Card Number should be a 16 digit number.')])
    cvv = StringField('CVV', validators=[DataRequired(), Regexp('^[0-9]{3}$',message='Your Card Security Code should be a 3 digit number.')])
    expiry_month = StringField('Exp Month', validators=[DataRequired(), Regexp('0[1-9]|1[0-2]',message="Expiry Month Should be a number between 01 and 12.")])
    expiry_year = StringField('Exp Year', validators=[DataRequired(), Regexp('^[0-9]{4}$',message='Expiry Year should be a 4 digit number.')])
    submit = SubmitField('Checkout')

class SearchForm(FlaskForm):
    search = StringField('Search Dogs', validators=[InputRequired(),Regexp('^[a-zA-Z ]+$',message='Search allows letters only')])
    submit = SubmitField('Search')
