# coding: utf-8

import math
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
    function(*args)
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

def mesure_time(methode, typeGen, nbTachesMax,nbInstances, step, debug=False,*args):
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
        sumTime = 0
        numTache += step
    return L_nbTaches, L_time

def save_graphe_data(filename, L_nbTaches, L_time, dirname='dataGraphe/'):
    if not(os.path.exists(dirname)):
        os.mkdir(dirname)
    fichier = dirname + filename
    f = open(fichier, 'w')
    s1 = ''
    s2 = ''
    for i in range(len(L_time)):
        s1 += (str)(L_time[i]) + ' '
        s2 += (str)(L_nbTaches[i]) + ' '
    s1 = s1[:-1]
    s2 = s2[:-1]
    f.write(s1 + '\n')
    f.write(s2)
    print('les données sont sauvegardées avec succès !')
    f.close()
    

def draw(L_nbTaches, L_time,xlabel='nombre de taches', ylabel='temps de calcul'):
    plt.plot(L_nbTaches, L_time)
    plt.xlabel = xlabel
    plt.ylabel = ylabel
    print('xlabel : ', plt.xlabel)
    print('ylabel : ', plt.ylabel)
    plt.show()


def test():
    L1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    L2 = list(map(lambda x: x**2, L1))
    print(L1)
    print(L2)
    verifComplexite(L1, L2)
    
def verifComplexite(L_nbTaches, L_time):
    t1 = L_nbTaches[::]
    t2 = L_time[::]
    for i in range(len(t2)):
        n = t1[i]
        t2[i] = math.log(t1[i])
    q = math.sqrt((t2[3] - t2[2])**2 + (t2[3] - t1[2]) ** 2)
    print('q : ', q)
    draw(t1,t2)

def main():
    #L_nbTaches, L_time = mesure_time(projet.Johnson, 'type1', 200, 10, 5)
    #save_graphe_data('Johnson/n²', L_nbTaches, L_time)
    #L_nbTaches, L_time = mesure_time(arborescence.arborescence_resolve, 'type3', 9, 5, 1)
    #save_graphe_data('exacte_type3_b1', L_nbTaches, L_time)
    L_nbTaches, L_time = mesure_time(arborescence.arborescence_mix, 'type1', 9, 5, 1)
    save_graphe_data('mix_type1_b1', L_nbTaches, L_time)
    draw(L_nbTaches, L_time)
    print('L_nbTaches : ', L_nbTaches)
    print('L_time : ', L_time)

main()