#!/usr/bin/env python3

"""
2012-12-17
"""

import re

import logging
logging.basicConfig(level=logging.DEBUG)
dbg = logging.debug

def _prepare(in_list, method) :
	"""
	transform a list of pattern into a list of compiled regular expressions
	"""
	out_list = list()
	if isinstance(in_list, str) :
		in_list = [in_list,]
	try :
		for pattern in set(in_list)  :
			if method == 'glob' :
				pattern = "^" + pattern.replace('?', '.').replace('*', '.*') + "$"
			elif method == 'strict' :
				pattern = re.escape(pattern)
			elif method == 'regexp' :
				pass
			else :
				pattern = '.*' + re.escape(pattern) + '.*'
			out_list.append(re.compile(pattern))
	except TypeError :
		pass
	return out_list
	
def test_item(item, pattern_list) :
	out_flag = False
	for pattern in pattern_list :
		if pattern.search(item) != None :
			out_flag = True
	return out_flag

def select(in_set, white=None, black=None, method=None) :
	"""
	for a given set of strings, return a new set, keep item according to a white
	and black list. Give priority to black list : Select item if match on
	white list, except it match on black list
	"""
	
	if white == None and black == None :
		return set()
	
	white = _prepare(white, method)
	black = _prepare(black, method)
	
	out_set = in_set.copy()
	for i in in_set :
		if not test_item(i, white) :
			out_set.discard(i)
		if test_item(i, black) :
			out_set.discard(i)
	return out_set
	
def discard(in_set, black=None, white=None, method=None) :
	"""
	for a given set of strings, return a new set, discard item according to a
	white and black list. Give priority to white list : Discard item if it match
	the black list, except if it match the white list
	"""
	
	if white == None and black == None :
		return in_set.copy()
	
	white = _prepare(white, method)
	black = _prepare(black, method)
	
	out_set = set()
	for i in in_set :
		if not test_item(i, black) :
			out_set.add(i)
		if test_item(i, white) :
			out_set.add(i)	
	return out_set
	
if __name__ == '__main__' :
	in_set = {'ba', 'be', 'bi', 'pa', 'pe', 'pi', 'da', 'de', 'di'}

	print(select(in_set, ['*a', 'pe'], method='glob'))
	print(select(in_set, ['*a', 'pe'], ['b*'], method='glob'))

	print(discard(in_set, method='glob'))
	print(discard(in_set, ['*a', 'pe'], method='glob'))
	print(discard(in_set, ['*a', 'pe'], ['b*'], method='glob'))
