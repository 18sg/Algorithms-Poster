from pso import *

if __name__ == "__main__":
	def runVisualiser(f, no_steps, swarm_size):
		opt = WikiPSOOptimiser(f, swarm_size, 0.6, 1.0, 2.0)

		print no_steps
		print swarm_size
		def print_hook(type, **kwargs):
			if type == "update_particle":
				print  "%d\t%s\t%s"%(kwargs["steps"] + 1,
						     "\t".join(map(str, kwargs["x"])),
						     "\t".join(map(str, kwargs["v"]))
						     )
		opt.listen(print_hook)
		opt.run(RunNumberTimes(opt, no_steps))



	runVisualiser(SchafferF6(array([53, 24])), 300, 100)

