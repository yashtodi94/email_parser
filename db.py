from mysql.connector import MySQLConnection, Error
#from MySQLdb import escape_string
from dbconfig import read_db_config
from mysql.connector import *
from processing import escape

def connect():
	db_config = read_db_config()
	con = MySQLConnection(**db_config)
	cursor = con.cursor()
	return con, cursor
	
def insert_to_messages_table(**db_dict):
	
	con, cursor = connect()
	#if not check_messages_table(**db_dict):
	query = """INSERT IGNORE INTO messages(user_contextio_uuid, user_email, msg_id, date_received, date_indexed, from_email, subject, order_id, store) VALUES ('{user_contextio_uuid}', '{user_email}', '{msg_id}', '{date_received}', '{date_indexed}', '{from_email}', '{subject}', '{order_id}', '{store}')""".format(**db_dict)
	cursor.execute(query)
	con.commit()
	con.close()
	return

def check_messages_table(**db_dict):
	con, cursor = connect()
	#query = """'SELECT * FROM messages WHERE msg_id = %s', (db_dict['msg_id'],)"""
	query = """SELECT (1) FROM messages WHERE msg_id = '{msg_id}'""".format(**db_dict)
	cursor.execute(query)
	con.close()
	#cursor.execute('SELECT * FROM messages WHERE msg_id = %s', (db_dict['msg_id'],))
	if cursor.fetchone():
		return True
	else:
		return False

def check_items_table(**db_dict):
	con, cursor = connect()
	#query = """'SELECT * FROM messages WHERE msg_id = %s', (db_dict['msg_id'],)"""	
	query = """SELECT (1) FROM items WHERE order_id = '{order_id}' AND item_title = '{item_title}'""".format(**db_dict)
	#cursor.execute("""SELECT * FROM items WHERE order_id = %s AND item_title = %s""", (db_dict['order_id'], db_dict['item_title']))
	cursor.execute(query)
	con.close()
	row = cursor.rowcount
	if row == 0:
		return True
	else:
		return False

def get_item_status(**db_dict):
	con, cursor = connect()
	if check_items_table(**db_dict):
		query = """SELECT item_status FROM items WHERE order_id = '{order_id}' AND item_title = '{item_title}'""".format(**db_dict)
		cursor.execute(query)
		con.close()
		return cursor.fetchone()[0]
	return False

def get_item_price(**db_dict):
	con, cursor = connect()
	if check_items_table(**db_dict):
		query = """SELECT item_price FROM items WHERE order_id = '{order_id}' AND item_title = '{item_title}'""".format(**db_dict)
		cursor.execute(query)
		con.close()
		print cursor.fetchone()[0]
		return cursor.fetchone()[0] == 0
	return False


def get_item_title(**db_dict):
	con, cursor = connect()
	#if check_items_table(**db_dict):
	query = """SELECT item_title FROM items WHERE order_id = '{order_id}' AND store = '{store}'""".format(**db_dict)
	cursor.execute(query)
	con.close()
	if cursor.rowcount:
		#print cursor
		titles = list()
		for row in cursor:
			titles.append(row[0])
		return titles
	else:
		print "False"
		return False

def insert_to_items_table(**db_dict):
	"""for key in db_dict:
		print key, db_dict[key]"""
	con, cursor = connect()

	#if not check_items_table(**db_dict):
	query = """INSERT IGNORE INTO items(user_email, order_id, item_title, item_price, delivery_address, item_status, store, user_contextio_uuid) VALUES('{user_email}', '{order_id}', '{item_title}', {item_price}, '{delivery_address}', '{item_status}', '{store}', '{user_contextio_uuid}')""".format(**db_dict)
	cursor.execute(query)
	con.commit()
	con.close()
	return


'''
def update_item_status(**db_dict):
	possible_item_status = ['confirmed', 'shipped', 'delivered', 'cancelled', 'returned']
	con, cursor = connect()
	#current_status = possible_item_status.index(get_item_status(**db_dict))
	#new_status = possible_item_status.index(db_dict["item_status"])
	current_status = 0
	if check_items_table(**db_dict):
		print "True"
		current_status = possible_item_status.index(get_item_status(**db_dict))
		new_status = possible_item_status.index(db_dict["item_status"])
		if new_status > current_status: 
			query = """UPDATE items SET item_status = '{item_status}' WHERE order_id = '{order_id}' AND item_title = '{item_title}'""".format(**db_dict)
			cursor.execute(query)
			print "Status update Item Title: ", db_dict["item_title"]
			con.commit()
			con.close()
	else:
		con.close()
		insert_to_items_table(**db_dict)
		#update_item_status(**db_dict)
		return
'''


def update_item_price(**db_dict):
	con, cursor = connect()
	#print "foo"
	if get_item_price(**db_dict):
		print "foo2"
		query = """UPDATE items SET item_price = '{item_price}' WHERE order_id = '{order_id}' AND item_title = '{item_title}'""".format(**db_dict)
		cursor.execute(query)
	con.commit()
	con.close()
	return

def update_item_status(**db_dict):
	possible_item_status = ['confirmed', 'shipped', 'delivered', 'cancelled', 'returned']
	con, cursor = connect()
	#current_status = possible_item_status.index(get_item_status(**db_dict))
	#new_status = possible_item_status.index(db_dict["item_status"])
	#current_status = 0
	#print "True"
	#current_status = possible_item_status.index(get_item_status(**db_dict))
	if (not get_item_status(**db_dict)):
		query = """INSERT IGNORE INTO items(user_email, order_id, item_title, item_price, delivery_address, item_status, store, user_contextio_uuid) VALUES('{user_email}', '{order_id}', '{item_title}', {item_price}, '{delivery_address}', '{item_status}', '{store}', '{user_contextio_uuid}')""".format(**db_dict)
		cursor.execute(query)
		#print "Status update Item Title: ", db_dict["item_title"]
		con.commit()
		con.close()
	else:
		current_status = possible_item_status.index(get_item_status(**db_dict))
		print "current status: ", possible_item_status[current_status]
		new_status = possible_item_status.index(db_dict["item_status"].strip().lower())
		if new_status > current_status: 
			query = """INSERT INTO items(user_email, order_id, item_title, item_price, delivery_address, item_status, store, user_contextio_uuid) VALUES('{user_email}', '{order_id}', '{item_title}', {item_price}, '{delivery_address}', '{item_status}', '{store}', '{user_contextio_uuid}') ON DUPLICATE KEY UPDATE item_status = '{item_status}'""".format(**db_dict)
			cursor.execute(query)
			print "Status update Item Title: ", db_dict["item_title"]
			con.commit()
			con.close()
	return
