from flask_wtf import Form
from wtforms import StringField, SelectField, DecimalField


class SearchForm(Form):
	"""Advanced Search form"""
	item_id = StringField('Item ID')
	description = StringField('Key Word')
	category = StringField('Item category')
	min_price = DecimalField('Min Price', default=0.0)
	max_price = DecimalField('Max Price', default=1000000.0)
	status = SelectField('Status', choices=[('upcoming', 'upcoming'), ('open', 'open'), ('closed', 'closed')])
