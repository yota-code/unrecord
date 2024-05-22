#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm



svg_header = '''
<svg
	xmlns="http://www.w3.org/2000/svg"
	version="1.1"
	width="4500px">
'''

svg_footer = '''
</svg>
'''

class Writer() :
	def __init__(self, name) :
##		if name[-4:] != '.svg' :
##			name += '.svg'
		self.name = name

		self.time = dict()
		self.data = dict()

		self.width = 4000
		self.heigth = 2000

	def __setitem__(self, key, value) :
		self.time[key] = value[0]
		self.data[key] = value[1]

	def __getitem__(self, key) :
		x = self.time[key]
		y = self.data[key]
		return x, y


	def get_window(self, x_min=None, x_max=None, y_min=None, y_max=None) :

		for i in self.data :
			u = self.data[i].max()
			y_max = u if y_max == None else max(u, y_max)
			
			d = self.data[i].min()
			y_min = d if y_min == None else max(d, y_min)

		for i in self.time :
			r = self.data[i].max()
			x_max = r if x_max == None else max(r, x_max)
			
			l = self.data[i].min()
			x_min = l if x_min == None else max(l, x_min)

	def x_format(self, x) :
		pass

	def dump(self) :
		fig = plt.figure(figsize=(12,6), dpi=100)
		prop = fm.FontProperties(size=11)
		axe = fig.add_subplot(1,1,1)
		for c in sorted(self.data.keys()) :
			axe.plot(self.time[c], self.data[c], label=c)

		#box = axe.get_position()
		#axe.set_position([box.x0, box.y0, box.width * 0.8, box.height])

		#axe.legend(loc='center left', bbox_to_anchor=(1, 0.5))
		axe.legend(loc='best', prop=prop)

		#axe.legend()
		#plt.show()
		plt.savefig(self.name)
		#fig.close()
		
	

if __name__ == '__main__' :
	
	fig = plt.figure(figsize=(4,4))
	#fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylabel('ylabel')
	ax.plot([1,2,4,3])
	plt.show()
