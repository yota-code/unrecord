#!/usr/bin/env python3

import os
import zlib
import pickle
import shutil
import tarfile
import tempfile
import collections

import logging
logging.basicConfig(level=logging.DEBUG)
dbg = logging.debug

import numpy as np



class Pack() :
	def __init__(self) :		
		self.data = dict() # variable -> np.array()
		self.meta = dict() # variable -> dict( time, unit, etc... )
		
		
		
		self.time = dict() # variable -> corresponding time vector name
		self.unit = dict() # variable -> unit
		self.variables = list() # list of available data, in order
		
	def set_variable(self, name, data, unit=None, time=None) :
		if name not in self.variables :
			self.variables.append(name)
		self.data[name] = data
		self.time[name] = time
		self.unit[name] = unit
		
	def get_timeline(self, variable) :
		return self.data[self.time[variable]]
		
	def __getitem__(self, variable) :
		dbg("> Pack.__getitem__({0})".format(variable))
		#if variable not in self.data and self.unpacked and variable in self.header :
		#	with tarfile.open(self.pack_pth, 'r') as tar_fid :
		#		data_fid = tar_fid.extractfile(self.get_id(variable))
		#		data_array = np.fromstring(bz2.decompress(data_fid.read()), dtype=self.header[variable]['dtype'])
		#		data_fid.close()
		#		self.data[variable] = np.load()
		return self.get_timeline(variable), self.data[variable]
	
	def load(self, pack_pth) :
		dbg("> Pack.load()")
		with tarfile.open(pack_pth, 'r') as tar_fid :
			self.time, self.unit, self.variables = pickle.load(tar_fid.extractfile('header.pickle'))
			# y aurait ptet moyen d'etre plus sioux avec le mode mmap
			with np.load("data.npz") as npz_fid :
				self.data = dict(npz_fid)
		dbg("Pack.load() <")
		return self
			
	def dump(self, pack_pth) :
		dbg("> Pack.dump()")
		
		tmp_dir = tempfile.mkdtemp()
		tmp_fid, tmp_pth = tempfile.mkstemp(dir=tmp_dir)
		
		# header preparation
		header_pth = os.path.join(tmp_dir, "header.pickle")
		header = (self.time, self.unit, self.variables, self.meta)
		with open(header_pth, 'wb') as header_fid :
			pickle.dump(header, header_fid, pickle.HIGHEST_PROTOCOL)
		
		# data preparation
		data_pth = os.path.join(tmp_dir, "data.npz")
		np.savez_compressed(data_pth, ** self.data)
		
		with tarfile.open(tmp_pth, 'w') as pack_fid :
			pack_fid.add(data_pth, arcname="data.npz")
			pack_fid.add(header_pth, arcname="header.pickle")
			
		shutil.move(tmp_pth, pack_pth)
		
		dbg("Pack.dump <")
		
if __name__ == '__main__' :
	u = Pack()
	
	u.set_variable("TIME", np.arange(10), "s", "TIME")
	u.set_variable("machin", np.sin(np.arange(10)), "truc", "TIME")
	u.set_variable("bidule", np.cos(np.arange(10)), "zut", "TIME")
	
	print(u['TIME'], u['machin'])
	u.dump("machintruc.pack")
	
	u.load("machintruc.pack")
	print(u['TIME'], u['machin'])
	
	
