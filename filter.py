#!/usr/bin/env python3

import math
import numpy as np

def _normal_distribution(x, sigma, mu) :
	
	g = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
	h = -1.0 * (2.0 * (sigma ** 2))

	return g * math.exp(((x - mu) ** 2) / h)

def _prepare_mask(a, radius) :

	one_a = np.ones_like(a, dtype=np.double)

	mask_coef = np.vstack((
		np.hstack((
			np.zeros(radius),
			one_a,
			np.zeros(radius)
		))
		for i in range(-1 * radius, radius + 1)
	))

	mask_value = np.vstack((
		np.hstack((
			np.zeros(radius + i),
			one_a,
			np.zeros(radius - i)
		))
		for i in range(-1 * radius, radius + 1)
	))

	return mask_value * mask_coef

	

def gaussian(a, radius=3, sigma=2.5) :
	
	a = np.asarray(a, dtype=np.double)
	one_a = np.ones_like(a, dtype=np.double)
	
	mask = _prepare_mask(a, radius)

	coef = np.vstack((
		np.hstack((
			np.zeros(radius),
			one_a * _normal_distribution(i, sigma, 0),
			np.zeros(radius)
		))
		for i in range(-1 * radius, radius + 1)
	))

	value = np.vstack((
		np.hstack((
			np.zeros(radius + i),
			a,
			np.zeros(radius - i)
		))
		for i in range(-1 * radius, radius + 1)
	))


	value_sum = (value * coef * mask).sum(axis=0)[radius:-radius]
	coef_sum = (coef * mask).sum(axis=0)[radius:-radius]

	return value_sum / coef_sum

		
if __name__ == '__main__' :
	import matplotlib.pyplot as plt
	import random
	u = [math.tanh(x/10.0) + 0.3 * ((random.random()**2) - 0.5) for x in range(-100,100)]
	v = gaussian(u, 5)
	plt.plot(u)
	plt.plot(v)
	plt.show()


