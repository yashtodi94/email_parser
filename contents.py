from processing import escape
import sys

def check_html(body):
	for i in range(len(body)):
		if body[i]["type"] == "text/html":
			#print i
			return i
	return False




def extract_contents(messages_obj):
	html_status = check_html(messages_obj.body)
	msg_fields = dict()
	#sys.stdout = open("op2", "w")
	if html_status != False:
		msg_fields["body"] = messages_obj.body[html_status]["content"]
		#print messages_obj.body
		
		msg_fields["body_type"] = messages_obj.body[html_status]["type"]
		#sys.stdout = open("op2", "a")
		#print messages_obj.body[html_status]
		msg_fields["date_received"] = messages_obj.date
		msg_fields["date_indexed"] = messages_obj.date_indexed
		msg_fields["msg_id"] = messages_obj.message_id
		addresses = messages_obj.addresses
		msg_fields["from_email"] = addresses["from"]["email"]
		msg_fields["subject"] = messages_obj.subject
		msg_fields["subject"] = escape(msg_fields["subject"])
		#print "Subject: ", msg_fields["subject"]
		#sys.exit(0)
		return msg_fields
	else:
		msg_fields["body"] = messages_obj.body[0]["content"]
		#print messages_obj.body
		
		msg_fields["body_type"] = messages_obj.body[0]["type"]
		#sys.stdout = open("op2", "a")
		#print messages_obj.body[0]
		msg_fields["date_received"] = messages_obj.date
		msg_fields["date_indexed"] = messages_obj.date_indexed
		msg_fields["msg_id"] = messages_obj.message_id
		addresses = messages_obj.addresses
		msg_fields["from_email"] = addresses["from"]["email"]
		msg_fields["subject"] = messages_obj.subject
		msg_fields["subject"] = escape(msg_fields["subject"])
		#print "Subject: ", msg_fields["subject"]
		#sys.exit(0)			
		return msg_fields
		
	#else:
	#return False
	#print msg_fields["body"]
	#print messages_obj.body
	#sys.exit(0)
	

#extract_contents(body)


