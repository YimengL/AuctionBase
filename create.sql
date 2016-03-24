create table Users (
	user_id text primary key,
	rating real,
	location text,
	country text
);

create table Items (
	item_id text primary key,
	seller_id text references Users(user_id),
	name text,
	buy_price real,
	first_bid real,
	currently real,
	number_of_bids int,
	started datetime,
	ends datetime,
	description text,
	check(started < ends)
);

create table Categories (
	item_id text references Items(item_id),
	category text,
	primary key (item_id, category)
);

create table Bids (
	item_id text references Items(item_id),
	user_id text references Users(user_id),
	time datetime,
	amount real,
	primary key (item_id, user_id, time)
);
