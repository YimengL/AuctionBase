select count(distinct Items.seller_id)
from Items join Bids
on Items.seller_id = Bids.user_id;
