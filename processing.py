import re
from mysql.connector import conversion
from mysql.connector import *


def str_process(str_list):
	for x in range(len(str_list)):
		str_list[x] = str_list[x].strip()
	str_list = filter(None, str_list)
	#for x in range(len(str_list)):
	string = ' '.join(str_list)
	#string.replace("'", "''")
	return string

def amount_process(amt):
	try:
		clean = re.sub(r'[^0-9.]', '', str(amt))
		clean = clean.lstrip('.')
		return float(clean)
	except:
		return amt

def escape(string):
	#string.MySQL.escape_string()
	#string = string.decode('string_escape')
	string = string.encode('unicode-escape').replace("'", "''")
	string = string.encode('unicode-escape').replace('"', '\"')
	#string = string.encode('unicode-escape').replace("'", u"\u2019")
	#string = string.encode('unicode-escape').replace('''"''', u"\u201D")
	#string = string.encode('unicode-escape').replace('''''', u"\u201D")
	return string
