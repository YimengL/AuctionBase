from peewee import *		# Using peewee ORM

DATABASE = SqliteDatabase('test.sqlite')

class User(Model):
	
	user_id = TextField(primary_key=True)
	rating = DoubleField()
	location = TextField(null=True)
	country = TextField(null=True)
	
	class Meta:
		database = DATABASE
		db_table = 'users'


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


class Category(Model):
	
	item_id = TextField()
	category = TextField()
	
	class Meta:
		database = DATABASE
		db_table = 'categories'
		primary_key = CompositeKey('item_id', 'category')


class Bid(Model):
	
	item_id = TextField()
	user_id = TextField()
	time = DateTimeField()
	amount = DoubleField()
	
	class Meta:
		database = DATABASE
		db_table = 'bids'
		primary_key = CompositeKey('item_id', 'user_id', 'time')


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Item, Category, Bid], safe=True)
	DATABASE.close()
