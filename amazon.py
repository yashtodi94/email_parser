import libxml2
import lxml
from lxml import html
import xml.etree.ElementTree as ET
from db import *
from regex_test import *
from bs4 import BeautifulSoup
import sys
from processing import *

class Amazon(object):
	def __init__(self):
		pass

	def amazon_extract_details(self, msg_fields, order_xpath, msg_params, acc_params):
		messages_dict = dict()
		items_dict = dict()
		messages_dict = {'store': 'Amazon'}
		messages_dict.update(msg_fields)
		messages_dict.update(acc_params)
		messages_dict["user_contextio_uuid"] = messages_dict.pop("id")
		items_dict["store"] = messages_dict["store"]
		items_dict["user_contextio_uuid"] = messages_dict["user_contextio_uuid"]
		items_dict["user_email"] = messages_dict["user_email"]
		
		if "out for delivery" in msg_fields["subject"].strip():
			return False
		if "could not be delivered" in msg_fields["subject"].strip():
			return False
		if "not available" in msg_fields["subject"].strip():
			return False
		if "kindle" in msg_fields["subject"].strip().lower():
			return False
		if "was refused" in msg_fields["subject"].strip().lower():
			return False
		if msg_params["sender"] == "auto-confirm@amazon.in" and "your order with amazon.in" in msg_fields["subject"].strip().lower():
			return False
		if "cheque tracking number" in msg_fields["subject"].strip().lower():
			return False
		if "important product safety" in msg_fields["subject"].strip().lower():
			return False
		if "cashback" in msg_fields["subject"].strip().lower():
			return False
		if "cancellation" in msg_fields["subject"].strip().lower():
			return False
		if "could not be delivered" in msg_fields["body"].strip():
			return False
		if "rescheduled the delivery" in msg_fields["body"].strip():
			return False

		#print msg_fields["subject"]

		if msg_fields["body_type"] == "text/plain":
			#print msg_fields["body"]
			if msg_params["sender"] == "order-update@amazon.in":
				#if "has delivered" in msg_fields["body"]:
				print msg_fields["subject"]
				items_dict["order_id"] = orderID_extractor(msg_fields["body"])
				items_dict["item_title"] = title_extractor(msg_fields["body"])
				items_dict["item_status"] = 'delivered'
				items_dict["item_price"] = 0
				items_dict["delivery_address"] = "foo"
				#print items_dict["order_id"], items_dict["item_title"]
		
			
		elif msg_fields["body_type"] == "text/html":
		
		#items_dict = self.xpath_processing(msg_fields["body"], order_xpath, **items_dict)
		#print msg_fields["subject"]
			tree = html.fromstring(msg_fields["body"])
			address = tree.xpath(order_xpath["address"])
			order_id = tree.xpath(order_xpath["order_id"])
			item_title = tree.xpath(order_xpath["item_title"])
		#print type(item_title), item_title[0]
		
		#print item_title
		#print msg_fields["msg_id"]
		#print msg_fields["date_received"]
			if "item_price" in order_xpath:	
				item_price = tree.xpath(order_xpath["item_price"])
				#print item_price	
				item_price = amount_process(item_price[0])
				items_dict["item_price"] = item_price
			else:
				items_dict["item_price"] = 0
				#print item_price
			items_dict["delivery_address"] = str_process(address)
			items_dict["item_title"] = str_process(item_title)
		#print item_title
		
			items_dict["item_title"] = escape(items_dict["item_title"])
			items_dict["order_id"] = str(order_id[0])
			#print items_dict["order_id"]
		messages_dict["order_id"] = items_dict["order_id"]
		
		if msg_params["sender"] == "auto-confirm@amazon.in":
			items_dict["item_status"] = 'confirmed'
			
			bsObj = BeautifulSoup(msg_fields["body"])
			order_total = bsObj.find("strong", text="Order Total:").findNext('td').get_text()
			order_total = amount_process(order_total)
			insert_to_messages_table(**messages_dict)
			update_item_status(**items_dict)
			update_item_price(**items_dict)
			#insert_to_items_table(**items_dict)
			#return
#			print "Order Total: " + str(order_total)
		elif msg_params["sender"] == "ship-confirm@amazon.in": #and "dispatched" in msg_fields["subject"].strip() or "shipped" in msg_fields["subject"].strip().lower():
			#print msg_fields["subject"]
			items_dict["item_status"] = 'shipped'
			#insert_to_items_table(**items_dict)
			insert_to_messages_table(**messages_dict)
			update_item_status(**items_dict)
			update_item_price(**items_dict)
			#return
		elif msg_params["sender"] == "order-update@amazon.in":
			if "delivered" in msg_fields["subject"].strip() or "has delivered" in msg_fields["body"]:
				items_dict["item_status"] = 'delivered'
				items_dict["item_price"] = 0
				#print msg_fields["msg_id"]
				#insert_to_items_table(**items_dict)
				insert_to_messages_table(**messages_dict)
				update_item_status(**items_dict)
				#return
		else:
			return False
		return



"""print "\n\n"
		print "Items Dictionary"
		for key in items_dict:
			print key, items_dict[key]
		
		print "\n\nMessages Dictionary"
		for key in messages_dict:
			if key is not "body":
				print key, messages_dict[key]
		"""

