#!/usr/bin/env python3

class GenericReader() :
	def __init__(self, filename, lazy=2) :
		
		self.filename = filename
		self.lazy = lazy
		
		self._data = dict()
		self._time = dict()

		self.variable_list = list()
		self.variable_unit = dict()
		
		self.parse_lazy()
		
	def parse_lazy(self, lazy) :
		if 1 <= lazy :
			self.parse_header()
		if 0 <= lazy :
			self.parse_data()

	def understand(self, filename) :
		# return 1.0 if the file can be understood by the reader
		return 0.0
		
	def __iter__(self) :
		self.parse_header()
		# mandatory! yield the variable names
		for varname in self.variable_list :
			yield varname
			
	def __getitem__(self, varname) :
		self.parse_data()
		# mandatory! return time vector and data array (np.array)
		return t, x

	def parse_header(self) :
		if self.lazy <= 1 : return
		# header parsing code here
		self.lazy = 1
		
	def parse_data(self) :
		if self.lazy <= 0 : return
		# data parsing code here
		self.lazy = 0

