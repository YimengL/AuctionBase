from flask.ext.login import UserMixin
from peewee import *		# Using peewee ORM


DATABASE = SqliteDatabase('test.sqlite')

class User(UserMixin, Model):
	
	user_id = TextField(primary_key=True)
	rating = DoubleField()
	location = TextField(null=True)
	country = TextField(null=True)
	
	class Meta:
		database = DATABASE
		db_table = 'users'
	
	
	def get_id(self):
		return self.user_id
	
	@classmethod
	def create_user(cls, user_id, location, country):
		if country == "":
			country = None
		if location == "":
			location = None
		try:
			with DATABASE.transaction():
				cls.create(user_id=user_id, location=location, country=country, rating=50.0)
		except IntegrityError:
			raise ValueError("User already exists")


class Item(Model):
	
	item_id = TextField(primary_key=True)
	seller_id = TextField()
	name = TextField()
	buy_price = DoubleField(null=True)	# The price, chosen by the seller before
										# the auction starts, at which a bidder
										# can win the auction immediately.
	first_bid = DoubleField()	# The minimum qualifying first-bid amount
	currently = DoubleField()	# The current highest bid
	number_of_bids = IntegerField()
	started = DateTimeField()
	ends = DateTimeField()
	description = TextField()
	
	class Meta:
		database = DATABASE
		db_table = 'items'
		constraints = [SQL('foreign key (seller_id) references users(user_id)'),
						Check('started < ends')]
	
	@classmethod
	def create_item(cls, item_id, seller_id, name, buy_price, first_bid, started, ends, description):
		if buy_price == "":
			buy_price = None
		try:
			with DATABASE.transaction():
				cls.create(item_id=item_id, seller_id=seller_id, name=name, buy_price=buy_price, first_bid=first_bid, currently=first_bid, number_of_bids=0, started=started, ends=ends, description=description)
		except IntegrityError:
			raise ValueError("User already exists")


class Category(Model):
	
	item_id = TextField()
	category = TextField()
	
	class Meta:
		database = DATABASE
		db_table = 'categories'
		primary_key = CompositeKey('item_id', 'category')
		constraints = [SQL('foreign key (item_id) references items(item_id)')]


class Bid(Model):
	
	item_id = TextField()
	user_id = TextField()
	time = DateTimeField()
	amount = DoubleField()
	
	class Meta:
		database = DATABASE
		db_table = 'bids'
		primary_key = CompositeKey('item_id', 'time')
		constraints = [SQL('foreign key (item_id) references items(item_id)'),
		SQL('foreign key (user_id) references users(user_id)')]
	
	@classmethod
	def create_bid(cls, item_id, user_id, time, amount):
		try:
			with DATABASE.transaction():
				cls.create(item_id=item_id, user_id=user_id, time=time, amount=amount)
		except IntegrityError:
			raise ValueError("Someone else bid this item at the same time, please change the current time first!")


class Time(Model):
	
	cur_time = DateTimeField(primary_key=True)
	
	class Meta:
		database = DATABASE
		db_table = 'times'
	
	@classmethod
	def create_time(cls, time):
		try:
			with DATABASE.transaction():
				cls.create(cur_time=time)
		except IntegrityError:
			raise ValueError("Already has this time")


def initialize():
	"""Create Database and Tables"""
	DATABASE.connect()
	DATABASE.create_tables([User, Item, Category, Bid, Time], safe=True)
	DATABASE.close()
