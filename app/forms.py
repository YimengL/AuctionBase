from flask_wtf import Form
from wtforms import StringField, SelectField, DecimalField, DateTimeField, TextField
from wtforms.validators import DataRequired, ValidationError

from models import User, Bid, Item


def userid_exists(form, field):
	"""helper function to check if user id is unique"""
	if User.select().where(User.user_id == field.data).exists():
		raise ValidationError("User with that id already exists.")


class SearchForm(Form):
	"""Advanced Search form"""
	item_id = StringField('Item ID')
	description = StringField('Key Word')
	category = StringField('Item category')
	min_price = DecimalField('Min Price', default=0.0)
	max_price = DecimalField('Max Price', default=1000000.0)
	status = SelectField('Status', choices=[('upcoming', 'upcoming'), ('open', 'open'), ('closed', 'closed')])


class RegisterForm(Form):
	user_id = StringField('User ID', validators=[DataRequired(), userid_exists])
	location = StringField('Location')
	country = StringField('Country')


class LoginForm(Form):
	"""Simple version of Login Form, only need id"""
	user_id = StringField('User ID')


class TimeForm(Form):
	"""Using this form to change the current time"""
	cur_time = DateTimeField('New DateTime', format="%Y-%m-%d %H:%M:%S")


class BidForm(Form):
	"""Using this form to bid the specific item"""
	amount = DecimalField('Price')


class ItemForm(Form):
	"""Using this form to place new items"""
	name = StringField("Item Name", validators=[DataRequired()])
	buy_price = DecimalField("Buy Price")
	first_bid = DecimalField("First Bid", validators=[DataRequired()])
	started = DateTimeField("Start Bid Date, format: 2000-11-08 21:21:21", format="%Y-%m-%d %H:%M:%S")
	ends = DateTimeField("End Bid Date, format: 2000-11-08 21:21:21", format="%Y-%m-%d %H:%M:%S")
	description = TextField("Description")
