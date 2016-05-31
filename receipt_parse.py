import sys
import json
from amazon import *
from paytm import *
from flipkart import *
from processing import escape
from contents import extract_contents
import libxml2
import lxml
from lxml import html
import xml.etree.ElementTree as ET
import yaml
import io
#import db_insert
from mysql.connector import MySQLConnection, Error
from requests import ConnectionError
from dbconfig import read_db_config
import re
from bs4 import BeautifulSoup
import contextio as c

#Add contextio consumer key and secret

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

context_io = c.ContextIO(
    consumer_key=CONSUMER_KEY, 
    consumer_secret=CONSUMER_SECRET
)

params = dict()
msg_params = dict()
acc_params = dict()
order_email_ids = dict()
db_list = list()
store_email_ids = dict()
order_xpath = dict()
details_xpath = dict()
msg_fields = dict()

with open('params.yaml', 'r') as f:
    params = yaml.load(f)

with open('order_email_ids.yaml', 'r') as f:
	store_email_ids = yaml.load(f)

with open('details_xpath.yaml', 'r') as f:
	details_xpath = yaml.load(f)

def sync(account_obj):
	syncing = account_obj.post_sync()
	#sync_status = syncing.get_sync()
	return syncing['success']

def params_assignment(initial_params_dict, target_params_dict):
	for key, value in initial_params_dict.iteritems():
		if value is not None:
			target_params_dict[key] = value
	return target_params_dict

#Initialize valid parameters for messages and account
msg_params = params_assignment(params["message_params"], msg_params)
acc_params = params_assignment(params["account_params"], acc_params)



print "Account Parameters:"
for key in acc_params:
	print key, acc_params[key]


print "\nMessage Parameters:"
for key in msg_params:
	print key, msg_params[key]


account = c.Account(context_io, acc_params)

#check if account exists:
if not account:
	sys.exit()

#populate details of account and display the email address of mailbox
try:
	account.get()
except ConnectionError:
	print "\nConnect to the Internet"
	sys.exit(0)


acc_params["user_email"] = str(account.email_addresses[0])
print "\n" + acc_params["user_email"]

#Trigger a sync



def main(sender):
	sync_status = sync(account)
	#Check if syncing was successful:
	if sync_status:
		print "Sync Status: " + str(sync_status)
		#Get messages from the account as per the parameters:
		messages = account.get_messages(**msg_params)
		ama = Amazon()
		paytm = Paytm()
		#If messages are fetched, extract the required contents else exit
		if messages:
			for items in range(len(messages)):
				msg_fields = extract_contents(messages[items])
				if msg_fields:
				
				#messg_id = msg_fields["msg_id"]
				#print messg_id
					
					#flipkart = Flipkart()
					if "amazon" in sender:
						if not ama.amazon_extract_details(msg_fields, order_xpath, msg_params, acc_params):
							continue
					#if not flipkart.flipkart_extract_details(msg_fields, order_xpath, msg_params, acc_params):
					#	continue
					if "paytm" in sender:
						if not paytm.paytm_extract_details(msg_fields, order_xpath, msg_params, acc_params):
							continue
				
				#paytm = Paytm()
				
				#insert_urls(messg_id, urls)
				
				#db_list.append(extract_contents(messages[items]))				
				
		else:
			print "\nNo messages found"
			sys.exit()
	else:
		print "\nSyncing failed: Exiting now"
		sys.exit()



#main

for key in store_email_ids:
	order_email_ids = params_assignment(store_email_ids[key], order_email_ids)
	for key2 in order_email_ids:
		msg_params["sender"] = order_email_ids[key2]
		print msg_params["sender"]
		order_xpath = params_assignment(details_xpath[msg_params["sender"]], order_xpath)
		main(msg_params["sender"])

"""
bsObj = BeautifulSoup(msg_fields["body"])

order_total = bsObj.findAll(text="Order Total")
print order_total	
print order_total[0].get_text()
"""
#print bsObj


