from flask import Flask, render_template, g
from flask.ext.bootstrap import Bootstrap

import models
import datetime

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

ITEMS_PER_PAGE = 15

app = Flask(__name__)
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
	items_stream = models.Item.select().limit(100).paginate(page, ITEMS_PER_PAGE)
	return render_template('items_stream.html', items_stream=items_stream)


@app.route('/about')
def about():
	"""The usage of this demo application"""
	return render_template('about.html')


@app.route('/item/<item_id>')
def item(item_id):
	"""show the exact item based on the item id"""
	item = models.Item.get(item_id=item_id)
	return render_template('item.html', item=item)



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
