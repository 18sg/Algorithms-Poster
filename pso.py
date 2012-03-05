#!/usr/bin/env python2
from numpy import array
import numpy as np
from math import *
import csv

class Function(object):
	"""A function to optimise. Has a number of dimensions, and can be called."""
	
	def __init__(self, n_dims):
		self.n_dims = n_dims
	
	def __call__(self, args):
		"""Call the function. args chould be a numpy array."""
		raise NotImplementedError()


class Polynomial(Function):
	
	def __init__(self, n_dims, minimum):
		Function.__init__(self, n_dims)
		self.minimum = minimum
	
	def __call__(self, args):
		return np.sum((args - self.minimum) ** 2)


class SchafferF6(Function):
	
	def __init__(self, minimum):
		Function.__init__(self, 2)
		self.minimum = minimum
	
	def __call__(self, args):
		(x, y) = args - self.minimum
		temp1 = sin(sqrt(x * x + y * y))
		temp2 = 1 + 0.001 * (x * x + y * y)
		return 0.5 + (temp1 * temp1 - 0.5) / (temp2 * temp2)


class EventEmitter(object):
	
	def __init__(self):
		self.listeners = []
	
	def listen(self, f):
		self.listeners.append(f)
	
	def emit(self, **kwargs):
		for listener in self.listeners:
			listener(**kwargs)


class StoppingCondition(object):
	
	def __init__(self, optimiser):
		self.optimiser = optimiser
	
	def step(self):
		raise NotImplementedError()


class RunNumberTimes(StoppingCondition):
	
	def __init__(self, optimiser, n):
		StoppingCondition.__init__(self, optimiser)
		self.n = n
	
	def step(self):
		self.n -= 1
		return self.n >= 0


class Optimiser(EventEmitter):
	"""A generic optimisation function."""
	
	def __init__(self, f):
		EventEmitter.__init__(self)
		self.f = f
		self.best = None
		self.steps = 0
	
	def run(self, condition):
		"""Run while the condition holds."""
		while condition.step():
			self.step()
			self.steps += 1
	
	def step(self):
		"""Perform one step of the algorithm."""
		raise NotImplementedError()


class Particle(object):
	"""Particles have a position, x, a velovity, v, and a best seen position, p."""
	
	def __init__(self, swarm):
		self.swarm = swarm
		self.x = np.random.uniform(-1, 1, self.swarm.f.n_dims)
		self.v = np.random.uniform(-1, 1, self.swarm.f.n_dims)
		self.p = np.copy(self.x)


class PSOOptimiser(Optimiser):
	"""A generic (ish) particle swarm optimiser."""
	
	def __init__(self, f, n_particles):
		Optimiser.__init__(self, f)
		self.n_particles = n_particles
		
		self.best = None
		
		self.particles = []
		for i in range(n_particles):
			particle = Particle(self)
			self.particles.append(particle)
			
			if self.best is None or self.f(particle.x) < self.f(self.best):
				self.best = np.copy(particle.x)
	
	def step(self):
		for i, particle in enumerate(self.particles):
			self.update_vel(particle)
			particle.x += particle.v
			self.emit(type="update_particle", n=i, x=particle.x, v=particle.v,
					y=self.f(particle.x), steps=self.steps)
			
			if self.f(particle.x) < self.f(particle.p):
				particle.p = np.copy(particle.x)
				if self.f(particle.p) < self.f(self.best):
					self.best = particle.p
					self.emit(type="update_best", n=i, x=self.best,
							y=self.f(self.best), steps=self.steps)
	
	def update_vel(self, particle):
		raise NotImplementedError()


class WikiPSOOptimiser(PSOOptimiser):
	"""The optimiser given in the wikipedia article."""
	
	def __init__(self, f, n_particles, weight_vel, weight_local, weight_global):
		PSOOptimiser.__init__(self, f, n_particles)
		self.weight_vel = weight_vel
		self.weight_local = weight_local
		self.weight_global = weight_global
	
	def update_vel(self, p):
		rp = np.random.uniform(0, 1, self.f.n_dims)
		rg = np.random.uniform(0, 1, self.f.n_dims)
		
		p.v = ( self.weight_vel    *      p.v
		      + self.weight_local  * rp * (p.p - p.x)
		      + self.weight_global * rg * (self.best - p.x)
		      )


if __name__ == "__main__":
	def run(f, f_name):
		csv_f = csv.DictWriter(open(f_name, "w"), "steps n y type".split(), extrasaction="ignore")
		csv_f.writeheader()
		
		def print_hook(type, **kwargs):
			if type == "update_best":
				csv_f.writerow(
						dict(steps=kwargs["steps"], y=kwargs["y"], n="best", type="best"))
			elif type == "update_particle":
				csv_f.writerow(
						dict(steps=kwargs["steps"], y=kwargs["y"], n=kwargs["n"], type="particle"))
		
		opt = WikiPSOOptimiser(f, 100, 0.6, 1.0, 2.0)
		opt.listen(print_hook)
		opt.run(RunNumberTimes(opt, 300))
	
	print "f6..."
	run(SchafferF6(array([20, 0])), "sf6.csv")
	print "poly..."
	run(Polynomial(2, array([20, 0])), "poly.csv")
	
	# Produce a file containing all the minimums of the sf6 function.
	f = SchafferF6(array([0, 0]))
	csv_f = csv.DictWriter(open("f6_mins.csv", "w"), ["y"])
	csv_f.writeheader()
	for x in range(25):
		x *= pi
		csv_f.writerow(dict(y=f(array([x, 0]))))
