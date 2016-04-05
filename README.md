#### AuctionBase

*****
Database for checking the Ebay historic data. Final Project for Stanford course: [Introduction to Database (CS 145)](http://web.stanford.edu/class/cs145/)  

Technologies and tools used: **Python**, **SQLite**, **Flask**, **Bootstrap**.

Author: Yimeng Li  
Website: [http://yimengli.me/](http://yimengli.me/)
*****

##### Part 1.A: Examine the XML data files (Finished)
Using Given DTD file to validate the xml data.
```Bash
$ xmllint --valid --noout items-*.xml
```

##### Part 1.B: Design your relational schema (Finished)
- **Users(<u>User_ID</u>, Rating, Location, Country)**
- **Items(<u>Item_ID</u>, Seller_ID, Name, Buy_Price, First_Bid, Currently, Number_of_Bids, Started, Ends, Description)**
- **Categories(<u>Item_ID</u>, <u>Category</u>)**
- **Bids(<u>Item_ID</u>, <u>User_ID</u>, <u>Time</u>, Amount)**

##### Part 1.C: Write a data transformation program (Finished)
- Finish ```parser.py```. Use Command:
```Bash
python parser.py data/items-*.xml
```
to generate ```bids.dat```, ```items.dat```, ```users.dat```, ```categories.dat```.
- Use unix tool to eliminate duplicates.
```Bash
$ sort bids.dat | uniq > bids_uniq.dat
$ sort items.dat | uniq > items_uniq.dat
$ sort users.dat | uniq > users_uniq.dat
$ sort categories.dat | uniq > categories_uniq.dat
```

##### Part 1.D: Load your data into SQLite (Finished)
- Create the ```auctionbase.sqlite``` database using
```Bash
$ sqlite3 auctionbase.sqlite
```
- Finish ```create.sql```, ```drop.sql``` and ```load.txt``` to automate the table creation and [**data bulk-loading**](http://cs.stanford.edu/people/widom/cs145/sqlite/SQLiteLoad.html) processes.

- By running the
```Bash
$ sqlite3 auctionbase.sqlite < create.sql
$ sqlite3 auctionbase.sqlite < load.txt
```
The data would be imported from ```bids_uniq.dat```, ```items_uniq.dat```, ```users_uniq.dat```, ```categories_uniq.dat``` to ```auctionbase.sqlite```.

##### Part 1.E: Test your SQLite database (Finished)
Finish several ```SQL``` queries to verify the correctness of above steps. **Example**:
```Bash
$ sqlite3 auctionbase.sqlite < db/query7.sql
150
```

*****

##### Part 2.A: Current Time (Finished)
Create CurrentTime table: ```time.sql```, and load it into ```auctionbase.sqlite``` database.
```Bash
sqlite3 auctionbase.sqlite < time.sql
```

##### Part 2.B: Constraints and Triggers (paused)

*****

##### Part 3 Web Application
- Install [```flask```]() and [```peewee```](http://docs.peewee-orm.com/en/latest/) & Run simple hello app.  
- Translate the original ```create.sql``` to ```models.py```  

###### Require Functionality
+ Registration/Login/Logout/Personal Profile
+ Ability to manually change the "current time". (**FINISHED**)
+ Ability for auction users to enter bids on open auctions. (**FINISHED**)
+ Ability to browse auction of interest based on the following input parameters: (**FINISHED**)
    - item ID
    - category
    - item description
    - price
    - open/closed status
+ Ability to view all relevant information pertaining to a single auction. This should be displayed on an individual webpage, and it should display all of the information in your database pertaining to that particular item. In particular, this page should include: (**FINISHED**)
    - the auction's open/close status
    - the acution's bids. You should also display all relevant information for each bid, including:
        * the name of bidder
        * the time of the bid
        * the price of the bid
    - if the auction is closed, it should display the winner of the auction  
+ Check all the constraints  

###### Extra:

+ Support Pagination (**FINISHED**)
+ Host on Digital Ocean (**FINISHED**)
+ Friendly UI
+ Support place items

*****
