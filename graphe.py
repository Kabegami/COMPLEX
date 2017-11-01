import os
import time
import circuit
import projet
import arborescence
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['backend'] = "Qt4Agg"

def getTime(function, *args):
    start = time.time()
    res = function(*args)
    #print('res : ', res)
    end = time.time()
    return end - start

def getData(filename):
    f = open(filename,'r')
    matrice = []
    for line in f:
        matrice.append([float(x) for x in line.split(' ')])
    f.close()
    t1, t2 = matrice[0], matrice[1:]
    nbTaches = (int)(t1[0])
    M = np.array(t2)
    return nbTaches, M

def mesure_time(methode, typeGen, nbTachesMax,nbInstances, step,debug=False,*args):
    print('args : ', args)
    prefix = 'Instances/' + typeGen + '/' + 'instances'
    numTache = step
    L_time = []
    L_nbTaches = []
    sumTime = 0
    while (numTache <= nbTachesMax):
        directory = prefix + (str)(numTache) + '/'
        if debug:
            print('directory : ', directory)
        for i in range(nbInstances):
            filename = directory + 'test' + (str)(i)
            if debug:
                print('filename : ', filename)
            n, M = getData(filename)
            if debug:
                print('n : ', n)
            t = getTime(methode, n, M,*args)
            sumTime += t
        L_nbTaches.append(numTache)
        L_time.append(sumTime / (1.0 * nbInstances))
        numTache += step
    return L_nbTaches, L_time

def save_graphe_data(filename, L_nbTaches, L_time, dirname='dataGraphe/'):
    if not(os.path.exists(dirname)):
        os.mkdir(dirname)
    fichier = dirname + filename
    f = open(fichier, 'w')
    f.write(' '.join(L_nbTaches))
    f.write(' '.join(L_time))
    f.close()
    

def draw(L_nbTaches, L_time):
    plt.plot(L_nbTaches, L_time)
    plt.show()

def main():
    #L_nbTaches, L_time = mesure_time_approche(projet.Johnson, 'type1', 100, 10, 5)
    L_nbTaches, L_time = mesure_time(arborescence.arborescence_resolve, 'type1', 10, 5, 5)
    draw(L_nbTaches, L_time)
    print('L_nbTaches : ', L_nbTaches)
    print('L_time : ', L_time)

main()
