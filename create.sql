create table Users (
	user_id text primary key,
	rating real,
	location text,
	country text
);

create table Items (
	item_id text primary key,
	seller_id int,
	name text,
	buy_price text,
	first_bid real,
	currently real,
	number_of_bids int,
	started datetime,
	ends datetime,
	description text
);

create table Categories (
	item_id text,
	category text,
	primary key (item_id, category)
);

create table Bids (
	item_id text,
	user_id text,
	time datetime,
	amount real,
	primary key (item_id, user_id, time)
);
