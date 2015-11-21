# forms.py

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm(Form):
	name = TextField(
		'Username',
		validators = [DataRequired(),
		Length(min = 3, max = 25)]
	)
	email = TextField(
		'Email',
		validators = [DataRequired(),
		Email(),
		Length(min = 6, max = 40)]
	)
	password = PasswordField(
		'Password',
		validators = [DataRequired(),
		Length(min = 3, max = 20)])
	confirm = PasswordField(
		'Repeat Password',
		validators = [DataRequired(), EqualTo('password')]
	)

class LoginForm(Form):
	name = TextField(
		'Username', 
		validators = [DataRequired()])
	password = PasswordField(
		'Password',
		validators = [DataRequired(),
		Length(max = 40)])

class AddStataForm(Form):
	body = TextField(
		'Stata here',
		validators=[DataRequired(),
		Length(min = 3, max = 140000)]
		)