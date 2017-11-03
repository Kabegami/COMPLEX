from tools import *
from projet import *
from arborescence import *
from bornes import *
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

		start = time.time()
		Johnson(ntasks, AB)
		end = time.time()

		results.append(end - start)
		print(".", end="", flush=True)

	mean_time = np.mean(results)

	# print("Results: {}".format(results))
	print("\nMean: {:.3f} s [{}]. Total time: {}".format(mean_time, mean_time, sum(results)))
	print("------------------------------------------------------")

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
		print(".", end="", flush=True)

	mean_time = np.mean(results)

	print("\nMean: {:.3f} s [{}]. Total time: {}".format(mean_time, mean_time, sum(results)))
	# print("Number of nodes explored: {}".format(n_nodes))
	print("------------------------------------------------------")

	return results, mean_time


def mean_time(niter=100, max_ntasks=50, bench_f=bench_exact, boundary=None):
	results = list()
	gen_funcs = {
		'Données non-corrélées': genere1, 
		'Corrélation sur les durées d\'exécution': genere2, 
		'Corrélation sur les machines': genere3
	}

	for gen_name, gen_f in gen_funcs.items():
		d = {'name': gen_name, 'data': list()}

		for i in range(1, max_ntasks+1):
			kwargs = {'ntasks': i, 'datagen': gen_f, 'niter': niter}
			if boundary is not None: kwargs['boundary'] = boundary
			_, m = bench_f(**kwargs)
			d['data'].append((i, m))

		results.append(d)

	return results


def quality(niter=10, max_ntasks=6):
	results = list()
	gen_funcs = {
		'Données non-corrélées': genere1, 
		'Corrélation sur les durées d\'exécution': genere2, 
		'Corrélation sur les machines': genere3
	}
	print("----------------- quality benchmark ------------------")
	for gen_name, datagen in gen_funcs.items():
		d = {'name': gen_name, 'data': list()}
		print("gen_f: {}".format(datagen.__name__))
		for ntasks in range(1, max_ntasks+1):
			print("Iterating {} times with {} tasks.".format(niter, ntasks))
			res = list()
			for _ in range(niter):
				_, data_m = datagen(ntasks)
				M = np.array(data_m)
				X = list(range(ntasks))
				tree = Arbre(X, M, borneMax)
				Pt, _ = tree.resolve()
				Pj = Johnson(ntasks, retire_machine(M))

				solver_t = circuit.Circuit(Pt, M)
				solver_j = circuit.Circuit(Pj, M)

				tt = solver_t.resolve()
				tj = solver_j.resolve()
				# print("Solution exact: {}; solution Johnson: {}. Accuracy: {}.".format(tt, tj, tt/tj))
				res.append(tt/tj)
				print(".", end="", flush=True)
			d['data'].append((ntasks, np.mean(res)))
			print("")
		results.append(d)

	print("------------------------------------------------------")

	return results


# def all():
# 	niter = 100
# 	ntasks = 5
# 	gen_funcs = [genere1, genere2, genere3]
# 	boundaries = [b1]

# 	r_approx = []
# 	# bench approx
# 	for gen_f in gen_funcs:
# 		res, mtime = bench_approx(niter=niter, datagen=gen_f, ntasks=ntasks)
# 		r_approx.append({'gen': gen_f.__name__, 'res': res, 'mean_time': mtime})

# 	r_exact = []
# 	# bench exact
# 	for gen_f in gen_funcs:
# 		for b in boundaries:
# 			res, mtime = bench_exact(
# 				niter=niter,
# 				datagen=gen_f, 
# 				ntasks=ntasks, 
# 				boundary=b
# 			)
# 			r_approx.append({
# 				'gen': gen_f.__name__, 
# 				'res': res, 
# 				'mean_time': mtime,
# 				'boundary': b.__name__
# 			})

def plot_quality():
	results = quality()
	f = plt.figure(1)

	for i in range(len(results)):
		r = list(zip(*results[i]['data']))
		plt.plot(r[0], r[1], label=results[i]['name'])

	plt.legend()
	plt.xlabel("Nombre de tâches")
	plt.ylabel("Qualité de la solution approchée")

	f.show()

def plot_mean_time(results1, results2):
	f = plt.figure(1)

	for i in range(len(results1)):
		r1 = list(zip(*results1[i]['data']))
		print(r1)
		plt.plot(r1[0], r1[1], label="{} (b1)".format(results1[i]['name']))

	# f.show()
	# results = mean_time(bench_f=bench_approx, max_ntasks=400, niter=50)
	# f = plt.figure(2)

	for i in range(len(results2)):
		r2 = list(zip(*results2[i]['data']))
		plt.plot(r2[0], r2[1], label="{} (borneMax)".format(results2[i]['name']))
	
	plt.legend()
	plt.xlabel("Nombre de tâches")
	plt.ylabel("Temps moyen de résolution (secondes)")
	f.show()


if __name__ == "__main__":
	# plot_quality()
	results1 = mean_time(bench_f=bench_exact, max_ntasks=6, niter=20, boundary=b1)
	results2 = mean_time(bench_f=bench_exact, max_ntasks=6, niter=20, boundary=borneMax)
	res = plot_mean_time(results1, results2)

