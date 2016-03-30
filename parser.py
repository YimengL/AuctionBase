
"""
FILE: skeleton_parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012

Skeleton parser for cs145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the xml files store dollar value amounts in 
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the xml files store dates/ times in the form 
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)
5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or 
is not of #PCDATA type)
6) A function to get all elements of a specific tag name that are children of a
given element
7) A function to get only the first such child

Your job is to implement the parseXml function, which is invoked on each file by
the main function. We create the dom for you; the rest is up to you! Get familiar 
with the functions at http://docs.python.org/library/xml.dom.minidom.html and 
http://docs.python.org/library/xml.dom.html

Happy parsing!
"""

import sys
from xml.dom.minidom import parse
from re import sub

columnSeparator = "<>"
columnSeparator2 = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
			'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


"""
Returns true if a file ends in .xml
"""
def isXml(f):
    return len(f) > 4 and f[-4:] == '.xml'

"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
	elements = []
	children = elem.childNodes
	for child in children:
		if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
			elements.append(child)
	return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
	children = elem.childNodes
	for child in children:
		if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
			return child
	return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
	return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
	if len(elem.childNodes) == 1:
		return pcdata(elem) 
	return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
	curElem = getElementByTagNameNR(elem, tagName)
	if curElem != None:
		return pcdata(curElem)
	return ''

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
	if mon in MONTHS:
		return MONTHS[mon] 
	else:
		return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
	dttm = dttm.strip().split(' ')
	dt = dttm[0].split('-')
	date = '20' + dt[2] + '-'
	date += transformMonth(dt[0]) + '-' + dt[1]
	return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
	if money == None or len(money) == 0:
		return money
	return sub(r'[^\d.]', '', money)

# File Writing
items_file = open('items.dat', 'w')
categories_file = open('categories.dat', 'w')
users_file = open('users.dat', 'w')
bids_file = open('bids.dat', 'w')


def writeLine(lst, f_handler):
	line = columnSeparator.join(lst)
	line = line.replace("|", "_")
	line = line.replace("<>", "|")
#	print line
	f_handler.write(line + "\n")
#	print line


def writeUser(userid, rating, location, country):
	"""write data to the users.dat"""
	lst = [userid, rating, location, country]
	writeLine(lst, users_file)


def writeItem(item_id, userid, name, buy_price, first_bid, currently, number_of_bids, started, ends, description):
	"""write data to the items.dat"""
	lst = [item_id, userid, name, buy_price, first_bid, currently, number_of_bids, started, ends, description]
	writeLine(lst, items_file)

def writeCategory(item_id, category_lst):
	"""write data to the categories.dat"""
	lst = [item_id, None]
	for category in category_lst:
		lst[1] = category
		writeLine(lst, categories_file)


def writeBid(item_id, bidderid, time, amount):
	"""write data to the bids.dat"""
	lst = [item_id, bidderid, time, amount]
	writeLine(lst, bids_file)


def parseXml(f):
	"""
	Parses a single xml file. Currently, there's a loop that shows how to parse
	item elements. Your job is to mirror this functionality to create all of the necessary SQL tables
	"""
	dom = parse(f) # creates a dom object for the supplied xml file
	"""
	TO DO: traverse the dom tree to extract information for your SQL tables
	"""
	collection = dom.documentElement
	
	items = getElementsByTagNameNR(collection, "Item")
	for item in items:
#		print "*****Item*****"
		
		# all the elements in xml file
		if item.hasAttribute("ItemID"):
			item_id = item.getAttribute("ItemID")
		name = getElementTextByTagNameNR(item, 'Name')
		category_lst = list()
		categories = getElementsByTagNameNR(item, "Category")
		for category in categories:
			category_lst.append(getElementText(category))
		currently = transformDollar(getElementTextByTagNameNR(item, 'Currently'))
		buy_price = transformDollar(getElementTextByTagNameNR(item, "Buy_Price"))
		if buy_price == '':
			buy_price = "NULL"
		first_bid = transformDollar(getElementTextByTagNameNR(item, "First_Bid"))
		number_of_bids = getElementTextByTagNameNR(item, "Number_of_Bids")
		location = getElementTextByTagNameNR(item, "Location")
		country = getElementTextByTagNameNR(item, "Country")
		started = transformDttm(getElementTextByTagNameNR(item, "Started"))
		ends = transformDttm(getElementTextByTagNameNR(item, "Ends"))
		seller = getElementByTagNameNR(item, "Seller")
		if seller.hasAttribute("UserID"):
			userid = seller.getAttribute("UserID")
		if seller.hasAttribute("Rating"):
			rating = seller.getAttribute("Rating")
		description = getElementTextByTagNameNR(item, "Description")
		
		
		bids = getElementByTagNameNR(item, "Bids")
		bid = getElementsByTagNameNR(bids, "Bid")
		if len(bid) > 0:
			for b in bid:
				bidder = getElementByTagNameNR(b, "Bidder")
				if bidder.hasAttribute("UserID"):
					bidderid = bidder.getAttribute("UserID")
				if bidder.hasAttribute("Rating"):
					bidder_rating = bidder.getAttribute("Rating")
				bidder_location = getElementTextByTagNameNR(bidder, "Location")
				if bidder_location == '':
					bidder_location = "NULL"
				bidder_country = getElementTextByTagNameNR(bidder, "Country")
				if bidder_country == '':
					bidder_country = "NULL"
				time = transformDttm(getElementTextByTagNameNR(b, "Time"))
				amount = transformDollar(getElementTextByTagNameNR(b, "Amount"))

				# write into dat file
				writeUser(bidderid, bidder_rating, bidder_location, bidder_country)
				writeBid(item_id, bidderid, time, amount)


		# Write into dat file
		writeUser(userid, rating, location, country)
		writeItem(item_id, userid, name, buy_price, first_bid, currently, number_of_bids, started, ends, description)
		writeCategory(item_id, category_lst)


"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""
def main(argv):
	if len(argv) < 2:
		print >> sys.stderr, 'Usage: python skeleton_parser.py <path to xml files>'
		sys.exit(1)
	# loops over all .xml files in the argument
	for f in argv[1:]:
		if isXml(f):
			parseXml(f)
			print "Success parsing " + f
	# close the file
	items_file.close()
	users_file.close()
	categories_file.close()
	bids_file.close()

if __name__ == '__main__':
	main(sys.argv)
