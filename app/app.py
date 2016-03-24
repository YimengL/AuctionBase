from flask import Flask, render_template, g

import models

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)

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
def index():
	"""root controller"""
	return render_template('index.html')



"""
Run the application
"""
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, host=HOST, port=PORT)
