select count(*) 
from ( 
	select item_id
	from Categories
	group by item_id
	having count(category) = 4);
