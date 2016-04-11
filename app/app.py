import datetime
from random import randint

from flask import Flask, render_template, g, request, url_for, redirect, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user

import models
import forms


DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

ITEMS_PER_PAGE = 15

app = Flask(__name__)
app.secret_key = "random"		# wtf-form require a secret_key
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'	# useful when adding
login_manager.login_message_category = "info"		# category of the flash message


@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get(models.User.user_id == user_id)
	except models.DoesNotExist:
		return None


@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE		# g is global
	g.db.connect()
	g.user = current_user
	g.cur_time = models.Time.select().limit(1).get().cur_time


@app.after_request
def after_request(response):
	"""Close the database connection after each request"""
	g.db.close()
	return response


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash("Congrat, you've registered", "success")
		models.User.create_user(
			user_id=form.user_id.data,
			location=form.location.data,
			country=form.country.data
		)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""login the AuctionBase Application"""
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.user_id == form.user_id.data)
		except models.DoesNotExist:
			flash("Your id is not in our record", "danger")
		else:
			login_user(user)
			flash("You've been logged in!", "success")
			return redirect(url_for('index'))
	
	return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	print "logout"
	logout_user()
	flash("You've been logout! Come back soon!", "success")
	return redirect(url_for('index'))


@app.route('/')
@app.route('/index/')
@app.route('/index/<int:page>')
def index(page=1):
	"""
	root controller
	render all the bids data on page
	"""
	cnt = models.Item.select().count()
	items_stream = models.Item.select().order_by(models.Item.ends.desc()).paginate(page, ITEMS_PER_PAGE)
	pages = (models.Item.select().count() - 1) / ITEMS_PER_PAGE + 1
	
	if cnt == 0:
		s_point = e_point = 0
	else:
		s_point = (page - 1) * ITEMS_PER_PAGE + 1
		e_point = min(page * ITEMS_PER_PAGE, cnt)
		
	return render_template('items_stream.html', items_stream=items_stream, page=page, pages=pages, cnt=cnt, s_point=s_point, e_point=e_point)


@app.route('/about')
def about():
	"""The usage of this demo application"""
	return render_template('about.html')


@app.route('/select_time', methods=['POST', 'GET'])
@login_required
def select_time():
	"""change the current time, but it can't be backward"""
	form = forms.TimeForm()
	if form.validate_on_submit():
		if form.cur_time.data > g.cur_time:
			flash("Current Time is changed", "success")
			q = models.Time.update(cur_time=form.cur_time.data)
			q.execute()
			return redirect(url_for('index'))
		else:
			flash("Changing time backwards is not allowed!", "danger")
	return render_template('time.html', form=form)


@app.route('/item/<item_id>')
def item(item_id):
	"""show the exact item based on the item id"""
	item = models.Item.get(item_id=item_id)
	join_cond = (models.Category.item_id == models.Item.item_id)
	categories = models.Category.select().join(models.Item, on=join_cond).where(models.Item.item_id == item_id)
	
	join_cond2 = (models.Bid.item_id == item_id)
	bids = models.Bid.select().join(models.Item, on=join_cond2).where(models.Item.item_id == item_id).order_by(models.Bid.time.desc())
	
	return render_template('item.html', item=item, categories=categories, bids=bids)


def generate_id():
	"""generate an unique item id"""
	while True:
		num = randint(1000000000, 9999999999)
		if not models.Item.select().where(models.Item.item_id == str(num)).exists():
			return str(num)


@app.route('/place_item', methods=['POST', 'GET'])
@login_required
def place_item():
	"""authenticated user can place new items"""
	form = forms.ItemForm()
	
	if form.validate_on_submit():
		if form.started.data > form.ends.data:
			flash("end time can't prior to the start time")
			render_template('place_item.html', form=form)
		if form.ends.data < g.cur_time:
			flash("You can't place an auction had already ended")
			render_template('place_item.html', form=form)
		item_id = generate_id()
		models.Item.create_item(item_id=item_id, seller_id=g.user.user_id, name=form.name.data, buy_price=form.buy_price.data, first_bid=form.first_bid.data, started=form.started.data, ends=form.ends.data, description=form.description.data)
		flash("Congrat! You have placed an auction successfully!", "success")
		return redirect(url_for('item', item_id=item_id))
	return render_template('place_item.html', form=form)


@app.route('/bid/<item_id>', methods=['POST', 'GET'])
@login_required
def bid(item_id):
	"""bid the exact item based on the item id"""
	
	form = forms.BidForm()
	item = models.Item.get(item_id=item_id)
	if form.validate_on_submit():
		# no auction may have two bids at the exact same time
		if models.Bid.select().where(models.Bid.item_id == item_id, models.Bid.time == g.cur_time).exists():
			flash("No auction may have two bids at the exact same time, please select another time", "danger")
			return render_template('bid.html', item=item, form=form)
		
		# Any new bid for a particular item must have a higher amount
		# number of bids for that particular item.
		if form.amount.data <= item.currently:
			flash("Any new bid for a particular item must have a higher amount number of bids for that particular item.", "danger")
			return render_template('bid.html', item=item, form=form)
		
		models.Bid.create_bid(
			item_id=item_id,
			user_id=g.user.user_id,
			time=g.cur_time,
			amount=form.amount.data
		)
		
		# update the current highest price
		item.currently = form.amount.data
		q = models.Item.update(currently=form.amount.data).where(models.Item.item_id == item_id)
		q.execute()
		
		# if this bid's price is higher than the Item.buy_price, then the 
		# auction will be close, and the current user will win
		if item.buy_price != None and form.amount.data >= item.buy_price:
			q = models.Item.update(ends=g.cur_time).where(models.Item.item_id == item_id)
			q.execute()
		
		return redirect(url_for('item', item_id=item_id))
	if g.user.user_id == item.seller_id:
		flash("A user may not bid on an item he or she is also selling", "danger")
	elif g.cur_time < item.started:
		flash("This item will be opened in the future", "info")
	elif g.cur_time >= item.ends:
		flash("This auction was closed!", "danger")
	else:
		return render_template('bid.html', item=item, form=form)
	return redirect(url_for('item', item_id=item_id))


@app.route('/advanced_search/', methods=('POST', 'GET'))
def advanced_search():
	"""Advanced Search"""
	form = forms.SearchForm()
	form = forms.SearchForm()
	if form.validate_on_submit():
		return redirect(url_for('advanced_search_results', item_id=form.item_id.data or "null", description=form.description.data or "null", category=form.category.data or "null", min_price=form.min_price.data, max_price=form.max_price.data, status=form.status.data, page=1))
	return render_template('advanced_search.html', form=form)


@app.route('/advanced_search_results/<item_id>/<description>/<category>/<min_price>/<max_price>/<status>/<int:page>')
def advanced_search_results(item_id, description, category, min_price, max_price, status, page=1):
	"""Show the results of advanced, search"""
	result = models.Item.select().order_by(models.Item.ends.desc())
	
	# based on the item_id
	if item_id != "null":
		try:
			result = result.where(models.Item.item_id.contains(item_id))
		except models.DoesNotExist:
			pass
	
	# based on the description
	if description != "null":
		try:
			result = result.where(models.Item.description.contains(description))
		except models.DoesNotExist:
			pass
	
	# based on the category
	# select * from items join categories on items.item_id = 
	# categories.item_id and categories likes form.category.data
	if category != "null":
		try:
			join_cond = (models.Category.category.contains(category))
			result = result.join(models.Category, on=join_cond).distinct().where(models.Category.item_id == models.Item.item_id)
		except models.DoesNotExist:
			pass

	# based on min price and max price
	try:
		result = result.where(models.Item.currently >= min_price, models.Item.currently <= max_price)
	except models.DoesNotExist:
		pass
	
	# based on the status
	try:
		cur_time = models.Time.select().limit(1)
		if status == "upcoming":
			result = result.where(models.Item.started > cur_time)
		elif status == "open":
			result = result.where(models.Item.started < cur_time, models.Item.ends > cur_time)
		else:		# closed
			result = result.where(models.Item.ends <= cur_time)
			
	except models.DoesNotExist:
		pass
	
	cnt = result.count()
	items_stream = result.paginate(page, ITEMS_PER_PAGE)
	pages = (result.count() - 1) / ITEMS_PER_PAGE + 1

	if cnt == 0:
		s_point = e_point = 0
	else:
		s_point = (page - 1) * ITEMS_PER_PAGE + 1
		e_point = min(page * ITEMS_PER_PAGE, cnt)
	
	cur_time = models.Time.select().limit(1).get().cur_time
	
	return render_template('advanced_search_results.html', items_stream=items_stream, page=page, pages=pages, item_id=item_id, description=description, category=category, min_price=min_price, max_price=max_price, status=status, cnt=cnt, s_point=s_point, e_point=e_point, cur_time=cur_time)


###############################################################


"""
Run the application
"""
if __name__ == '__main__':
	models.initialize()
	if models.Time.select().count() < 1:
		try:
			models.Time.create_time(datetime.datetime(2001, 12, 20, 0, 0, 1))
		except ValueError:
			pass
	app.run(debug=DEBUG, host=HOST, port=PORT)
