#!/usr/bin/env python3

"""
Reader for .see files
"""

import os, sys
import struct
import collections
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

class Reader() :
	def __init__(self, data_pth, timeline="TEMPS") :
		dbg("Reader.__init__({0})".format(data_pth))
		
		self.data_pth = os.path.abspath(data_pth)
		
		self.data = dict() # variable -> np.array()
		self._meta = collections.defaultdict(dict) # variable -> dict( time, unit, etc... )
		
		self._meta[None]['timeline'] = timeline
		
		self.variables = list()
		
		self.parse_header()
		self.parse_data()
		
	def meta(self, key, variable=None) :
		return self._meta[variable][key]
	
	def timeline(self, variable=None) :
		return self.data[self._meta[variable]['timeline']]
		
	def __getitem__(self, variable) :
		return self.timeline(variable), self.data[variable]
		
	def parse_header(self) :
		dbg("> Reader.parse_header()")
		
		with open(self.data_pth) as fid :
			self._meta['__global__']['title'] = fid.readline().strip()
			self._meta['__global__']['subtitle'] = fid.readline().strip()
			
			variable_line = [i.strip() for i in field_split(fid.readline().rstrip('\n'), 13)]
			unit_line = [i.strip() for i in field_split(fid.readline().rstrip('\n'), 13)]
			
		self.variables = variable_line
		for variable, unit in zip(variable_line, unit_line) :
			self._meta[variable]['unit'] = unit
		
	def parse_data(self) :
		dbg("> Reader.parse_data()")
		
		tmp_lst = list()
		with open(self.data_pth) as fid :
			for n, line in enumerate(fid) :
				if n < 4 :
					continue
				tmp_lst.append([literal_eval(i.strip()) for i in field_split(line, 13)])
		tmp_arr = np.array(tmp_lst)
		
		print(tmp_arr.shape)
		print(self.variables)
		for i, variable in enumerate(self.variables) :
			self.data[variable] = tmp_arr[:,i]

if __name__ == '__main__' :
	import matplotlib
	import matplotlib.pyplot as plt
	
	u = Reader(r"/U/chassagne/service/20140924_fenetra_obsolescence/example/Beep_ReposCRS_servo.see")
	v = Reader(r"/U/chassagne/service/20140924_fenetra_obsolescence/example/Beep_ReposCRS_servo_bis.see")

	var_list = ['CDT01', 'CDT02', 'CDTC1', 'CDTS1', 'CMDFOR', 'CMDLFT', 'CMDRHT', 'CMDTAL', 'POSFOR', 'POSLFT', 'POSRHT', 'POSTAL']
	
	matplotlib.rcParams.update({
		'axes.labelsize': 'small','axes.titlesize': 'small', 'xtick.labelsize':'small',
		'ytick.labelsize':'small', 'axes.grid': True
	})
	
	fig, axe = plt.subplots(4, 3, sharex=True, sharey=False, figsize=(11.57, 8.14))
	fig.suptitle("{0}".format(u.meta('title'), fontsize=18))
	
	for i in range(4):
		for j in range(3) :
			g = axe[i, j]
			line_ref, = g.plot(* u[var_list[3*i+j]], color='black')
			line_tst, = g.plot(* v[var_list[3*i+j]], color='red')
			g.set_title(var_list[3*i+j])
			g.margins(0.0, 0.05)
	
	fig.legend((line_ref, line_tst), ("Beep_ReposCRS_servo.see", "Beep_ReposCRS_servo_bis.see"), ncol=2, loc='lower center', fontsize=10)
	fig.tight_layout(rect=(0.0, 0.05, 1.0, 0.95))
	fig.subplots_adjust(wspace=0.15, hspace=0.20)
	fig.savefig("test.pdf")
	
