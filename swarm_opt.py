#!/usr/bin/python

import random
from math import sin, sqrt

################################################################################
# Function to minimise
################################################################################


def schafferF6(x, y):
	# Where the minimum will be
	x -= 10
	y -= 10
	
	temp1 = sin(sqrt(x * x + y * y))
	temp2 = 1 + 0.001 * (x * x + y * y)
	return 0.5 + (temp1 * temp1 - 0.5) / (temp2 * temp2)

def polynomial(x):
	# Where the minium will be
	x -= 0
	
	return x ** 2

# Select one from the above
f = schafferF6


################################################################################
# Model/Algorithm
################################################################################

class Particle(object):
	
	def __init__(self, swarm, best = None, position = None, velocity = None):
		self.swarm = swarm
		self.position = self._random_vector() if position is None else position
		self.velocity = self._random_vector() if velocity is None else velocity
		self.best     = self.position[:]      if best is None     else best
	
	
	def _random_vector(self):
		# Get a random vector of values -1 to 1
		return map((lambda _: (random.random()-0.5)*2), range(self.swarm.dimensions))
	
	
	def step(self):
		# Step the simulation on one timestep
		for dimension in range(self.swarm.dimensions):
			# Update velocity
			self.velocity[dimension] += (
				(2 * random.random() * (self.best[dimension] - self.position[dimension]))
				+
				(2 * random.random() * (self.swarm.best[dimension] - self.position[dimension]))
			)
			
			# Move
			self.position[dimension] += self.velocity[dimension]
		
		# Does this new position beat the previous best?
		if f(*self.position) < f(*self.best):
			self.best = self.position[:]
	
	
	# Compare this particle's current position with another's
	def __cmp__(self, other):
		delta = f(*self.position) - f(*other.position)
		if delta < 0:
			return -1
		elif delta == 0:
			return 0
		else:
			return 1
	
	
	# Produce a gnuplottable line containing:
	#   * time
	#   * position fields
	#   * velocity fields
	def __str__(self):
		return "%d\t%s\t%s"%(self.swarm.time,
		                     "\t".join(map(str, self.position)),
		                     "\t".join(map(str, self.velocity))
		                     )



class Swarm(object):
	
	def __init__(self):
		# Python magic... (Get the number of arguments our function takes
		import inspect
		self.dimensions = len(inspect.getargspec(f).args)
		
		self.particles = []
		self.best = None
		self.time = 0
	
	
	def add(self, particle):
		self.particles.append(particle)
		self._update_best()
	
	
	def _update_best(self):
		cur_best = min(self.particles).position
		
		if self.best is None or f(*cur_best) < f(*self.best):
			self.best = cur_best[:]
	
	
	def step(self):
		self.time += 1
		
		for particle in self.particles:
			particle.step()
		
		self._update_best()
	
	
	# The gnuplottable line for each particle
	def __str__(self):
		return "\n".join(map(str, self.particles))



################################################################################
# Experiment
################################################################################


# Generate a swarm
swarm = Swarm()
swarm_size = 100
for _ in range(swarm_size):
	swarm.add(Particle(swarm))


# Run the algorithm a few times

num_steps = 100
#print str(swarm)
for _ in range(num_steps):
	swarm.step()
	# Print the best we've found
	print "%d\t%s"%(swarm.time, "\t".join(map(str, swarm.best)))
	#print str(swarm)
