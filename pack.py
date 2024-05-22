#!/usr/bin/env python3

import os

import numpy as np
import logging

#import unrecord.plugin.res_b
import unrecord.plugin.see

handler_list = [
#	unrecord.plugin.res_b,
	unrecord.plugin.see
]

import unrecord.black_white

import re

logging.basicConfig(level=logging.DEBUG)
dbg = logging.debug

class Pack() :
	"""
	handle different parsers, hold data, can be lazy
	"""
	def __init__(self) :
		
		self.reader = dict()
		self.writer = dict()
		
		self.selected_variable = list()
		self.selected_datafile = list()

	def load_data(self, filename, nickname=None, handler=None) :
		filepack = os.path.abspath(filename) + '.pack'
		#if os.path.exists(filepack) :
		
		if handler == None :
			u = 0.0
			for h in handler_list :
				if h.Reader(filename).understand() > u :
					handler = h
		if nickname != None :
			nickname = '.'.join(os.path.basename(filename).split()[:-1])
		self.reader[nickname] = handler.Reader(filename)

		return self.reader[nickname]

	def dump_data(self, name) :
		if name[-4:] == '.svg' or name[-4:] == '.png' :
			handler = graphit
		try :
			self.writer[name] = handler.Writer(name)
			return self.writer[name]
		except :
			raise

	def dump_pack(self, pack_name=None) :
		if os.path.exists(self.pack_path) :
			os.remove(self.pack_path)
			
		pack_tar = tarfile.open(self.pack_path, 'w')
		
		for k in self.data :
			data_fname = self.get_id(k)
			data_path = os.path.join(self.tmp_dir, data_fname)
			data_fid = open(data_path, 'wb')
			data_fid.write(bz2.compress(self.data[k].tostring()))
			data_fid.close()
			pack_tar.add(data_path, arcname=data_fname)
		
		header_fname = '_header'
		header_path = os.path.join(self.tmp_dir, header_fname)
		header_fid = open(header_path, 'wb')
		pickle.dump(self.header, header_fid, pickle.HIGHEST_PROTOCOL)
		header_fid.close()
		pack_tar.add(header_path, arcname=header_fname)
		
	def load_pack(self, pack_name=None) :
		pass

	def select_variable(self, white=None, black=None) :
		pre_list = list()
		for datafile in self.selected_datafile :
			pre_list += list(self.reader[datafile])
			
		self.selected_variable = black_white.select(pre_list, white, black)

		return self.selected_variable

