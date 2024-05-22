import math
import matplotlib.pyplot as plt
import random
from filter import gaussian
import numpy as np

import warnings

warnings.simplefilter("ignore", RuntimeWarning)

class Tolerance() :
	def __init__(self, ref, tst, radius=10.0) :
		
		self.ref = np.array(ref)
		self.tst = np.array(tst)
		self.radius = radius

	def score_quadratic(self, p = 2.0) :

		d = (self.tst - self.ref) / self.radius
		
		a = np.absolute(d)
		a = math.pow((a ** p).sum() / len(self.ref), 1.0 / p)
		
		return 100.0 * a

	def score_hyperbolic(self) :

		d = (self.tst - self.ref) / self.radius
				
		a = np.absolute(1.0 / (d.clip(max=1.0) - 1.0))
		b = np.absolute(1.0 / (d.clip(min=-1.0) + 1.0))
		
		return (300.0/8.0) * ((a * b).sum() / len(self.ref))

	def plot(self, out=None, smooth=0) :
		
		fig = plt.figure()
		
		ax = fig.add_subplot('111')

		if smooth > 0 :
			self.ref_s = gaussian(self.ref, smooth)
		else :
			self.ref_s = self.ref
		
		lower = self.ref_s - self.radius
		upper = self.ref_s + self.radius
	
		ax.fill_between(x, lower, upper, alpha=0.2, color='green', edgecolor='black')
		ax.plot(x, self.ref, color='green')
		ax.plot(x, self.tst, color='blue')

		if out == None :
			plt.show()
		else :
			plt.savefig(out)
			
		plt.close()


if __name__ == '__main__' :
	
	radius = 1.0

	x = np.array([i / 25.0 for i in range(-50,51)])

	yref = [math.tanh(i) + random.normalvariate(0.0,0.1) for i in x]
	ytst = [math.tanh(i) + random.normalvariate(-0.5,0.2) for i in x]

	t = Tolerance(yref, ytst, radius)
	print(t.score_hyperbolic())
	print(t.score_quadratic())
	t.plot('test.svg', smooth=5)




