select count(distinct Items.seller_id)
from Users join Items
on Items.seller_id = Users.user_id and Users.rating > 1000;
