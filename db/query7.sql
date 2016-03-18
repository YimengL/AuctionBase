select count(distinct Categories.category)
from Categories join Items
on Categories.item_id = Items.item_id and Items.number_of_bids > 0 and Items.currently > 100;
