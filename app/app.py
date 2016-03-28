import datetime

from flask import Flask, render_template, g, request
from flask.ext.bootstrap import Bootstrap

import models
import forms


DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

ITEMS_PER_PAGE = 15

app = Flask(__name__)
app.secret_key = "random"		# wtf-form require a secret_key
bootstrap = Bootstrap(app)


@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE		# g is global
	g.db.connect()


@app.after_request
def after_request(response):
	"""Close the database connection after each request"""
	g.db.close()
	return response


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
	"""
	root controller
	render all the bids data on page
	"""
	items_stream = models.Item.select().paginate(page, ITEMS_PER_PAGE)
	pages = (models.Item.select().count() - 1) / ITEMS_PER_PAGE + 1
	return render_template('items_stream.html', items_stream=items_stream, page=page, pages=pages)


@app.route('/about')
def about():
	"""The usage of this demo application"""
	return render_template('about.html')


@app.route('/item/<item_id>')
def item(item_id):
	"""show the exact item based on the item id"""
	item = models.Item.get(item_id=item_id)
	return render_template('item.html', item=item)


@app.route('/advanced_search/', methods=('GET', 'POST'))
def advanced_search_results():
	"""Advanced Search"""
	form = forms.SearchForm()
	if form.validate_on_submit():
		result = models.Item.select()
		
		# based on the item_id
		try:
			result = result.where(models.Item.item_id.contains(form.item_id.data))
		except models.DoesNotExist:
			pass
		
		# based on the description
		try:
			result = result.where(models.Item.description.contains(form.description.data))
		except models.DoesNotExist:
			pass
		
		# based on the category
		# select * from items join categories on items.item_id = 
		# categories.item_id and categories likes form.category.data
		try:
			join_cond = (models.Category.category.contains(form.category.data))
			result = result.join(models.Category, on=join_cond).distinct().where(models.Category.item_id == models.Item.item_id)
		except models.DoesNotExist:
			pass
		
		# based on min price and max price
		try:
			result = result.where(models.Item.currently >= form.min_price.data, models.Item.currently <= form.max_price.data)
		except models.DoesNotExist:
			pass
		
		# based on the status
		try:
			cur_time = models.Time.select().limit(1)
			if form.status.data == "upcoming":
				result = result.where(models.Item.started > cur_time)
			elif form.status.data == "open":
				result = result.where(models.Item.started < cur_time, models.Item.ends > cur_time)
			else:		# closed
				result = result.where(models.Item.ends < cur_time)
				
		except models.DoesNotExist:
			pass
		
		return render_template('advanced_search_results.html', result=result)
	
	return render_template('advanced_search.html', form=form)


###############################################################

"""
Run the application
"""
if __name__ == '__main__':
	models.initialize() 
	try:
		models.Time.create_time(datetime.datetime(2001, 12, 20, 0, 0, 1))
	except ValueError:
		pass
	app.run(debug=DEBUG, host=HOST, port=PORT)
