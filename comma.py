import numpy as np
import heapq
import csv

class LibreOffice(csv.Dialect) :
	delimiter = ','
	doublequote = False
	escapechar = '\\'
	lineterminator = '\n'
	quotechar = '"'
	quoting = csv.QUOTE_NONNUMERIC
	skipinitialspace = True

class Reader() :
	pass

def interpolate_t(xa, xb, ya, yb, t) :
	x = (xa - xb) * t + xa
	y = (ya - yb) * t + ya

def interpolate_x(xa, xb, ya, yb, x) :
	t = (x - xa) / (xa - xb)
	y = (ya - yb) * t + ya

	return y

class Writer() :
	def __init__(self, name) :
		self.name = name

		self.data = dict()
		self.time = dict()

	def collapse_time(self) :
		time_set = set()
		for variable in self.time :
			time_set |= self.time[variable]
		return list(time_set).sort()

	def interpolate(self, variable, time) :
		pass

	def dump(self, selection_list=None) :
		time_list = self.collapse_time()
		with open(self.name, mode='wt', encoding='UTF-8') as fid :
			for t in time_list :
				pass
		


if __name__ == '__main__' :
	w = Writer('truite.csv')
	w.dump()
