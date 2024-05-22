#!/usr/bin/env python3


"""
Reader for .see files
"""

import os, sys
import struct
import collections

from pathlib import Path

import unrecord.plugin

import numpy as np

from ast import literal_eval

import logging
logging.basicConfig(level=logging.DEBUG)
dbg = logging.debug

def upfront(x) :
	i_prev = 0
	for n, i in enumerate(x) :
		if i_prev == 0 and i == 1 :
			return n
		i_prev = i

def field_split(line, c=None) :
	""" if c is an integer, split every c characters, else, use standard split function """
	try : 
		return line.split(c)
	except TypeError :
		try :
			return [line[i:i+c] for i in range(0, len(line), c)]
		except :
			return [line,]

class Reader(unrecord.plugin.GenericReader) :
	def __init__(self, file_pth, time_var="TEMPS") :
		dbg("Reader.__init__({0})".format(file_pth))
		
		self.data_pth = file_pth
		
		self.data = dict() # variable -> np.array()
		self.meta = collections.defaultdict(dict) # variable -> dict( time, unit, etc... )
		
		self.meta[None]['__time__'] = time_var
		
		self.variable_lst = list()
		
		self.parse_header()
		self.parse_data()
		
	def meta(self, key, variable=None) :
		return self.meta[variable][key]
	
	def time(self, variable=None) :
		return self.data[self.meta[None]['__time__']]
		
	def get(self, variable) :
		return self.time(variable), self.data[variable]
		
	def __getitem__(self, key) :
		return self.data[key]
		
	def __setitem__(self, key, value) :
		self.data[key] = value

	def parse_header(self) :
		dbg("Reader.parse_header()")
		
		with self.data_pth.open('rt', encoding='utf8') as fid :
			self.meta[None]['title'] = fid.readline().strip()
			self.meta[None]['subtitle'] = fid.readline().strip()
			
			variable_line = [i.strip() for i in field_split(fid.readline().rstrip('\n'), 13)]
			unit_line = [i.strip() for i in field_split(fid.readline().rstrip('\n'), 13)]
			
		self.variable_lst = variable_line
		for variable, unit in zip(variable_line, unit_line) :
			self.meta[variable]['unit'] = unit
			
	def restore_time(self, step=0.025) :
		self.data[self.meta[None]['__time__']] = np.arange(self.row_nbr) * step
		
	def parse_data(self) :
		dbg("Reader.parse_data()")
		
		tmp_lst = list()
		with self.data_pth.open('rt', encoding='utf8') as fid :
			for n, line in enumerate(fid) :
				if n < 4 :
					continue
				if not line.strip() :
					continue
				tmp_lst.append([literal_eval(i.strip())
					for i in field_split(line, 13)[:len(self.variable_lst)]
				])
		tmp_arr = np.array(tmp_lst)
		
		self.row_nbr, self.col_nbr = tmp_arr.shape
		
		for i, variable in enumerate(self.variable_lst) :
			self.data[variable] = tmp_arr[:,i]
			
	def compose(self, pth) :
		# TODO: sacrément beurk, créer une fonction field_join()
		with pth.open('wt', encoding='ascii') as fid :
			fid.write(self.meta[None]['title'] + '\n')
			fid.write(self.meta[None]['subtitle'] + '\n')
			fid.write(''.join(variable[:13].ljust(13) for variable in self.variable_lst) + '\n')
			fid.write(''.join(self.meta[variable]["unit"][:13].ljust(13) for variable in self.variable_lst) + '\n')
			for n in range(len(self.time())) :
				fid.write(''.join(str(self.data[variable][n])[:13].ljust(13) for variable in self.variable_lst) + '\n')
			
			


