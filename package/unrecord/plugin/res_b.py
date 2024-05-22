#!/usr/bin/env python3

"""
	Reader for enreg.res.b files
	
Le fichier est composé de la façon suivant :
- un champ texte pour le titre
- un champ text pour le sous-titre
- un entier pour le nombre de blocs
pour chaque bloc :
	- un champ d'entête contenant :
		- un entier pour l'identifiant du bloc
		- un entier pour le nombre de variables
		- le nom du bloc
	pour chaque variable :
		- un champ texte contenant le nom et l'unité
à partir de là se trouvent les données
jusqu'à la fin du fichier :
	- un entier pour l'identifiant du bloc
	- un flottant pour le temps courant
	- un champ binaire pour les valeurs enregistrées en flottant

sachant que les champs, texte ou binaires sont composés comme suit :
	- un entier pour la taille du champ
	- un champ, dont la taille en octets et connu
	- un entier dont la valeur doit être égale au premier

"""

import os, sys
import struct
import collections

import numpy as np

import unrecord.plugin

import logging
logging.basicConfig(level=logging.DEBUG)
dbg = logging.debug

def preview(s, i=200) :
	return str(s)[:i]

class Reader(unrecord.plugin.GenericReader) :
	
	marker_size = 4
	marker_type = '>I'
	endianness = '>'
	
	def __init__(self, filename) :
		self.filename = filename
		
		self._data = dict()
		self._time = dict()

		self.variable_list = list()
		self.variable_unit = dict()
		
		self.parse_header()
		self.parse_data()

	def understand(self, filename=None) :
		o = 1.0
		o *= 1.0 if filetype[-6:] =='.res.B' else 0.5
		o *= 1.0 if self.guess_type() else 0.0
		return o

	def __getitem__(self, varname) :
		block_ident = self.block_variable_to_ident[varname]
		t = self.block_ident_to_time[block_ident]
		x = self._data[varname]
		return t, x
	
	def guess_type(self, filename=None) :
		filename = filename if filename != None else self.filename
		with open(filename, 'rb') as fid :
			u = fid.read(8)
			if u[:8] == b'\x50\x00\x00\x00\x00\x00\x00\x00' :
				dbg("type: 8 byte marker, little endian")
				self.marker_size = 8
				self.marker_type = '<Q'
				self.endianness = '<'		
			elif u[:4] == b'\x00\x00\x00\x50' :
				dbg("type: 4 byte marker, big endian")
				self.marker_size = 4
				self.marker_type = '>I'
				self.endianness = '>'
			elif u[:4] == b'\x50\x00\x00\x00' :
				dbg("type: 4 byte marker, little endian")
				self.marker_size = 4
				self.marker_type = '<I'
				self.endianness = '<'
			else :
				dbg("type: unknown: {0}".format(u))
				return False
		return True

	def split_variable_unit(self, line) :
		return line[:-12].strip(), line[-12:].strip()
	
	def extract_chunk(self, fid) :
		try :
			m = fid.read(self.marker_size)
			block_len = struct.unpack(self.marker_type, m)[0]
		except struct.error :
			raise struct.error("no more block")

		block = fid.read(block_len)
		n = fid.read(self.marker_size)
		
		if m != n :
			raise ValueError("\n\tstart block len : {}\n\tbut end block len : {}".format(m, n))
		
		return block

	def parse_header(self) :
			
		self.guess_type()
	
		# for a given ident, return the number of variable in this block
		self.block_ident_to_variable_count = dict()
		# for a given ident, return the list of variable in this block
		self.block_ident_to_variable_list = collections.defaultdict(list)
		# for a given variable, return the ident of the block holding this variable
		self.block_variable_to_ident = dict()
		
		with open(self.filename, 'rb') as fid :
			
			self.title = self.extract_chunk(fid).decode('ascii')
			self.subtitle = self.extract_chunk(fid).decode('ascii')

			s = self.endianness + 'I'
			self.block_nbr = struct.unpack(s, self.extract_chunk(fid))[0]

			for i in range(self.block_nbr) :
				header = self.extract_chunk(fid)
				
				s = self.endianness + 'II'
				block_ident, variable_count = struct.unpack(s, header[:8])
				block_name = header[8:].decode('ascii').strip()

				block_key = (block_name, block_ident, variable_count)

				self.block_ident_to_variable_count[block_ident] = variable_count
						
				for j in range(variable_count) :
					line = self.extract_chunk(fid).decode('ascii')
					variable, unit = self.split_variable_unit(line)
					self.variable_unit[variable] = unit
					self._data[variable] = None
					self.variable_list.append(variable)
					self.block_ident_to_variable_list[block_ident].append(variable)
					self.block_variable_to_ident[variable] = block_ident

			self._data_from = fid.tell()

		dbg(preview(self.block_ident_to_variable_count))
		dbg(preview(self.block_ident_to_variable_list))
		dbg(preview(self.block_variable_to_ident))
				
		return self
		
	def parse_data(self) :
			
		self.block_ident_to_time = collections.defaultdict(list)
		data_raw = collections.defaultdict(bytearray)
		data_prepared = dict()
		
		with open(self.filename, 'rb') as fid :
			fid.seek(self._data_from)	
			while True :
				try :
					for i in range(self.block_nbr) :
						s = self.endianness + 'If'
						block_ident, time = struct.unpack(s, self.extract_chunk(fid))
						self.block_ident_to_time[block_ident].append(time)
						data_raw[block_ident] += bytearray(self.extract_chunk(fid))
				except struct.error :
					break
		
		for block_ident in data_raw :
			data_array = np.fromstring(bytes(data_raw[block_ident]) , dtype = self.endianness + 'f4')
			variable_count = (self.block_ident_to_variable_count[block_ident] - 1)
			sample_count = len(data_array) // variable_count
			data_prepared[block_ident] = np.reshape(data_array, (sample_count, variable_count))

		self._data = dict()
		for block_ident in self.block_ident_to_variable_list :
			for n, variable in enumerate(self.block_ident_to_variable_list[block_ident]) :
				self._data[variable] = data_prepared[block_ident][:, n-1]

		for block_ident in self.block_ident_to_time :
			self.block_ident_to_time[block_ident] = np.array(self.block_ident_to_time[block_ident], dtype=np.float32)
				
		return self
		
if __name__ == '__main__' :
	
	p = Reader(sys.argv[1]).parse_header().parse_data()
	print(p['BAFCS1'])

