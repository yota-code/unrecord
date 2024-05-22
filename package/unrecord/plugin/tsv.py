#!/usr/bin/env python3

import os, sys
import struct
import collections
import numpy as np
import ast

import unrecord.plugin

class Reader(unrecord.plugin.GenericReader) :
	def __init__(self, filename) :
		self.filename = filename
		
		self.parse()
		
	def parse(self) :
		with open(self.filename, 'rt', encoding='utf8') as fid :
			stack = [
				[
					cell.strip().replace('\\n', '\n').replace('\\t', '\t')
					for cell in line.rstrip('\n').split('\t')
				]
				for line in fid
			]
			
		self.header = stack[0]
		self.data = stack[1:]
		
		return self
		
	def __getitem__(self, name) :
		i = self.header.index(name)
		a = [ast.literal_eval(line[i]) for line in self.data]
		return np.arange(len(a)), np.array(a)
		

