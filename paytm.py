import libxml2
import lxml
from lxml import html
import xml.etree.ElementTree as ET
from processing import *
from db import *
from bs4 import BeautifulSoup

class Paytm(object):
	def __init__(self):
		pass

	def paytm_extract_details(self, msg_fields, order_xpath, msg_params, acc_params):
		messages_dict = dict()
		items_dict = dict()
		messages_dict = {'store': 'Paytm'}
		messages_dict.update(msg_fields)
		messages_dict.update(acc_params)
		messages_dict["user_contextio_uuid"] = messages_dict.pop("id")
		items_dict["store"] = messages_dict["store"]
		items_dict["user_contextio_uuid"] = messages_dict["user_contextio_uuid"]
		items_dict["user_email"] = messages_dict["user_email"]

		tree = html.fromstring(msg_fields["body"])

		if "items confirmed" in msg_fields["subject"].strip().lower():
			confirmed_dict = dict()
			items_dict, messages_dict = self.make_dict(tree, order_xpath["confirmed"], items_dict, messages_dict, "confirmed")
			#insert_to_items_table(**items_dict)	
			update_item_status(**items_dict)	
			
		elif "order shipped" in msg_fields["subject"].strip().lower():
			items_dict, messages_dict = self.make_dict(tree, order_xpath["shipped"], items_dict, messages_dict, "shipped")
			update_item_status(**items_dict)

		elif "order delivered" in msg_fields["subject"].strip().lower():
			items_dict, messages_dict = self.make_dict(tree, order_xpath["delivered"], items_dict, messages_dict, "delivered")
			update_item_status(**items_dict)
		elif "order cancelled" in msg_fields["subject"].strip().lower():
			subject = msg_fields["subject"].strip().lower()
			print subject
			try:
   				#items_dict["order_id"] = re.search("order(.+?)", subject).group(1)
				order_id_index = subject.find("order # ")
				items_dict["order_id"] = subject[(order_id_index + len("order # ")):len(subject)].strip()
				items_dict["order_id"].encode("utf-8")
				#items_dict["item_title"] = ""
				print items_dict["order_id"]
				messages_dict["order_id"] = items_dict["order_id"]
				titles = get_item_title(**items_dict)
				for i in range(len(titles)):
					if titles[i] in msg_fields["body"]:
						items_dict["item_title"] = titles[i]
						items_dict["item_status"] = "cancelled"
						items_dict["item_price"] = 0
						items_dict["delivery_address"] = "foo"
						update_item_status(**items_dict)
						insert_to_messages_table(**messages_dict)
				#items_dict["order_id"] = items_dict["order_id"].strip()
				#print items_dict["order_id"]
			except AttributeError:
				items_dict["order_id"] = "not found"
				print items_dict["order_id"]

	@classmethod
	def make_dict(self, tree, xpath_dict, items_dict, messages_dict, status):
		address = tree.xpath(xpath_dict["address"])
		order_id = tree.xpath(xpath_dict["order_id"])
		item_title = tree.xpath(xpath_dict["item_title"])
		item_price = tree.xpath(xpath_dict["item_price"])
		items_dict["item_price"] = amount_process(item_price)
		items_dict["item_title"] = str_process(item_title)
		items_dict["order_id"] = str_process(order_id)
		print items_dict["order_id"]
		#print address
		items_dict["delivery_address"] = str_process(address)
		print items_dict["delivery_address"]
		items_dict["item_status"] = status
		messages_dict["order_id"] = items_dict["order_id"]
		insert_to_messages_table(**messages_dict)
		return items_dict, messages_dict
"""
	@staticmethod
	def str_process(str_list):
		for x in range(len(str_list)):
			str_list[x] = str(str_list[x]).strip()
		str_list = filter(None, str_list)
		#for x in range(len(str_list)):
		string = ' '.join(str_list)
		return string

	@staticmethod
	def amount_process(amt):
		clean = re.sub(r'[^0-9.]', '', str(amt))
		clean = clean.lstrip('.')
		return float(clean)"""
