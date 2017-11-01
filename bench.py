from tools import *
from projet import *
from arborescence import *
from bornes import b1, b2
import time
import numpy as np
import matplotlib.pyplot as plt


def bench_approx(niter=100, datagen=genere1, ntasks=50):
	print("------------------ benchmark approx ------------------")
	print("Iterating {} times with {} tasks.".format(niter, ntasks))
	print("Function used for data generation: {}".format(datagen.__name__))

	results = []

	for _ in range(niter):
		_, data_m = datagen(ntasks)

		# init
		M = np.array(data_m)
		AB = retire_machine(M)
		X = [i for i in range(M.shape[1])]

		start = time.time()
		Johnson(X, AB)
		end = time.time()

		results.append(end - start)

	mean_time = np.mean(results)

	# print("Results: {}".format(results))
	print("Mean: {:.0f} s [{}]".format(mean_time, mean_time))
	print("------------------------------------------------------\n")

	return results, mean_time


def bench_exact(niter=100, datagen=genere1, ntasks=10, boundary=b1):
	print("------------------ benchmark exact -------------------")
	print("Iterating {} times with {} tasks.".format(niter, ntasks))
	print("Function used for data generation: {}".format(datagen.__name__))
	print("Boundary: {}".format(boundary.__name__))

	results = []

	for _ in range(niter):
		_, data_m = datagen(ntasks)

		# init
		M = np.array(data_m)
		X = list(range(ntasks))
		tree = Arbre(X, M, boundary)

		start = time.time()
		tree.resolve()
		end = time.time()

		results.append(end - start)

	mean_time = np.mean(results)

	print("Mean: {:.0f} s [{}]".format(mean_time, mean_time))
	print("------------------------------------------------------\n")

	return results, mean_time


def mean_time(niter=100, max_ntasks=50, bench_f=bench_exact):
	results = list()
	gen_funcs = [genere1, genere2, genere3]

	for gen_f in gen_funcs:
		d = {'gen_f': gen_f.__name__, 'data': list()}

		for i in range(1, max_ntasks+1):
			_, m = bench_f(ntasks=i, datagen=gen_f, niter=niter)
			d['data'].append((i, m))

		results.append(d)

	return results


def all():
	niter = 100
	ntasks = 5
	gen_funcs = [genere1, genere2, genere3]
	boundaries = [b1]

	r_approx = []
	# bench approx
	for gen_f in gen_funcs:
		res, mtime = bench_approx(niter=niter, datagen=gen_f, ntasks=ntasks)
		r_approx.append({'gen': gen_f.__name__, 'res': res, 'mean_time': mtime})

	r_exact = []
	# bench exact
	for gen_f in gen_funcs:
		for b in boundaries:
			res, mtime = bench_exact(
				niter=niter,
				datagen=gen_f, 
				ntasks=ntasks, 
				boundary=b
			)
			r_approx.append({
				'gen': gen_f.__name__, 
				'res': res, 
				'mean_time': mtime,
				'boundary': b.__name__
			})


if __name__ == "__main__":
	f = plt.figure(1)

	results = mean_time(bench_f=bench_approx)

	for i in range(3):
		r = list(zip(*results[i]['data']))
		plt.plot(r[0], r[1], label=results[i]['gen_f'])
	plt.legend()
	f.show()

