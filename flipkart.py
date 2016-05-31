import libxml2
import lxml
from lxml import html
from lxml.html.clean import Cleaner
import xml.etree.ElementTree as ET
from processing import *
from db import *
from bs4 import BeautifulSoup

class Flipkart(object):
	def __init__(self):
		pass

	def flipkart_extract_details(self, msg_fields, order_xpath, msg_params, acc_params):
		messages_dict = dict()
		items_dict = dict()
		messages_dict = {'store': 'Flipkart'}
		messages_dict.update(msg_fields)
		messages_dict.update(acc_params)
		messages_dict["user_contextio_uuid"] = messages_dict.pop("id")
		items_dict["store"] = messages_dict["store"]
		items_dict["user_contextio_uuid"] = messages_dict["user_contextio_uuid"]
		items_dict["user_email"] = messages_dict["user_email"]
		cleaner = Cleaner()
		cleaner.javascript = True
		cleaner.style = True

		tree = html.fromstring(msg_fields["body"])
		#print order_xpath
		if msg_params["sender"] == "noreply@flipkart.com" and "confirmation" in msg_fields["subject"].strip().lower():
			#tree = html.fromstring(msg_fields["body"])
			#address = tree.xpath(order_xpath["address"])
#			print order_xpath["address"]
			print msg_fields["subject"]
			#print address
			address = list()
			bsObj = BeautifulSoup(msg_fields["body"])
			add = bsObj.find(text="DELIVERY ADDRESS")
			
			if add:
				addr = add.findNext().get_text().encode("utf-8")
				#addr = addr.replace("\xa0", " ")
				address.append(addr)
				address.append(add.findNext().findNext().get_text().encode("utf-8"))
				print type(address)
				#print address
				items_dict["delivery_address"] = str_process(address)
				print items_dict["delivery_address"]
			else:
				items_dict["delivery_address"] = ""
			"""for x in range(len(order_xpath["order_id"])):
				order_id = tree.xpath(order_xpath["order_id"][x])
				if order_id:
					break"""
			order_id = re.search(r"\[(\w+)\]", msg_fields["subject"])
			items_dict["order_id"] = order_id.group(1)
			print items_dict["order_id"]
			items_dict["item_title"] = str_process(tree.xpath(order_xpath["item_title"]))
			print items_dict["item_title"]
			item_price = tree.xpath(order_xpath["item_price"])
			items_dict["item_price"] = amount_process(item_price)
			print items_dict["item_price"]
			items_dict["item_status"] = "confirmed"
			messages_dict["order_id"] = items_dict["order_id"]
			#insert_to_items_table(**items_dict)
			#insert_to_messages_table(**messages_dict)
			
			
			"""
			if "item_price" in order_xpath:	
				item_price = tree.xpath(order_xpath["item_price"])	
				item_price = amount_process(item_price)
				items_dict["item_price"] = item_price
				#print item_price
			items_dict["delivery_address"] = str_process(address)
			items_dict["item_title"] = str_process(item_title).strip()
			items_dict["order_id"] = order_id
			messages_dict["order_id"] = order_id
			items_dict["item_status"] = "confirmed"
			for key in items_dict:
				print key, items_dict[key]
			insert_to_items_table(**items_dict)
			insert_to_messages_table(**messages_dict)"""
