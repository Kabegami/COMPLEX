# coding: utf-8

import math
import os
import time
import circuit
import projet
import arborescence
import numpy as np
import bornes
import matplotlib.pyplot as plt
import approche
from scipy import stats
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

def read_graphe_file(*Lfilename):
    dirname = 'dataGraphe/'
    L = []
    time = []
    cpt = 1
    for filename in Lfilename:
        fichier = dirname + filename
        f = open(fichier, 'r')
        for line in f:
            if cpt % 2 != 0 or cpt == 2:
                L.append([float(x) for x in line.split(' ')])
            cpt += 1
        f.close()
    L_nbTaches = L[1]
    print(L_nbTaches)
    del L[1]
    return L_nbTaches, L   
    

def mesure_time(methode, typeGen, nbTachesMax,nbInstances, step, debug=False,*args):
    print('args : ', args)
    prefix = 'Instances/' + typeGen + '/' + 'instances'
    numTache = step
    L_time = []
    L_nbTaches = []
    sumTime = 0
    while (numTache <= nbTachesMax):
        #print('numTache : ', numTache)
        directory = prefix + (str)(numTache) + '/'
        if debug:
            print('directory : ', directory)
        for i in range(nbInstances):
            filename = directory + 'test' + (str)(i)
            if debug:
                print('filename : ', filename)
            n, M = getData(filename)
            print('n : ', n)
            t = getTime(methode, n, M,*args)
            sumTime += t
        L_nbTaches.append(numTache)
        L_time.append(sumTime / (1.0 * nbInstances))
        sumTime = 0
        numTache += step
    return L_nbTaches, L_time

def compare_methodes(methode1, methode2, name1, name2, nbTachesMax, nbInstances, step):
    L_label= ['',"Données non-corrélées", "Corrélation sur les durées d'éxécution", "Corrélation sur les machines"]
    for i in range(1,4):
        data_type = 'type' + (str)(i)
        L_nbTaches, L_time1 = mesure_time(methode1,data_type, nbTachesMax, nbInstances, step)
        L_nbTaches, L_time2 = mesure_time(methode2,data_type, nbTachesMax, nbInstances, step)
        plt.plot(L_nbTaches, L_time1, label=L_label[i] + ' ' + name1)
        plt.plot(L_nbTaches, L_time2, label=L_label[i] + ' ' + name2)
    plt.xlabel('Nombre de taches')
    plt.ylabel('Temps de calcul')
    plt.legend()
    plt.show()

def compare_node(methode1, methode2, name1, name2, nbTachesMax, nbInstances, step):
    L_label= ['',"Données non-corrélées", "Corrélation sur les durées d'éxécution", "Corrélation sur les machines"]
    for i in range(1,4):
        data_type = 'type' + (str)(i)
        L_nbTaches, L_time1 = mesure_node(methode1,data_type, nbTachesMax, nbInstances, step)
        L_nbTaches, L_time2 = mesure_node(methode2,data_type, nbTachesMax, nbInstances, step)
        plt.plot(L_nbTaches, L_time1, label=L_label[i] + ' ' + name1)
        plt.plot(L_nbTaches, L_time2, label=L_label[i] + ' ' + name2)
    plt.xlabel('Nombre de taches')
    plt.ylabel('Nombre de noeud explorés')
    plt.legend()
    plt.show()
    

def mesure_node(methode, typeGen, nbTachesMax, nbInstances, step, debug=False, *args):
    print('args : ', args)
    prefix = 'Instances/' + typeGen + '/' + 'instances'
    numTache = step
    L_cpt = []
    L_nbTaches = []
    sumCpt = 0
    while (numTache <= nbTachesMax):
        #print('numTache : ', numTache)
        directory = prefix + (str)(numTache) + '/'
        if debug:
            print('directory : ', directory)
        for i in range(nbInstances):
            filename = directory + 'test' + (str)(i)
            if debug:
                print('filename : ', filename)
            n, M = getData(filename)
            print('n : ', n)
            cpt =  methode(n, M,*args)
            sumCpt += cpt
        L_nbTaches.append(numTache)
        L_cpt.append(sumCpt / (1.0 * nbInstances))
        sumCpt = 0
        numTache += step
    return L_nbTaches, L_cpt    

def mesure_approximation(methode, typeGen, nbTachesMax, nbInstances, step, debug=False):
    #print('args : ', args)
    prefix = 'Instances/' + typeGen + '/' + 'instances'
    numTache = step
    L_exacte = []
    L_res = []
    L_nbTaches = []
    sumRes = 0
    sumExacte = 0
    while (numTache <= nbTachesMax):
        #print('numTache : ', numTache)
        directory = prefix + (str)(numTache) + '/'
        if debug:
            print('directory : ', directory)
        for i in range(nbInstances):
            filename = directory + 'test' + (str)(i)
            if debug:
                print('filename : ', filename)
            n, M = getData(filename)
            print('n : ', n)
            P =  methode(n, M)
            c = circuit.Circuit(P, M)
            res = c.resolve()
            opt, exacte = arborescence.arborescence_mix(n, M)
            #print('exacte : ', exacte)
            #print('opt ', opt)
            sumRes += res
            sumExacte += exacte
            
        L_nbTaches.append(numTache)
        L_exacte.append(2*(sumExacte / (1.0*nbInstances)))
        L_res.append(sumRes / (1.0*nbInstances))
        sumRes = 0
        sumExacte = 0
        numTache += step
    return L_nbTaches, L_res, L_exacte

def graphe_approximation(methode, name, numMax, nbInstances, step, xlabel='Nombre de taches', ylabel="Resultat de l'ordonnancement", courbe_label="type"):
    prefix = 'type'
    M = []
    for i in range(1,4):
        data_type = prefix + (str)(i)
        L_label= ['',"Données non-corrélées", "Corrélation sur les durées d'éxécution", "Corrélation sur les machines"]
        L_nbTaches, L_res, L_exacte = mesure_approximation(methode, data_type, numMax, nbInstances, step)
        #s = name + '_' + data_type
        plt.plot(L_nbTaches, L_res, label=L_label[i] + ' Johnson')
        plt.plot(L_nbTaches, L_exacte, label=L_label[i] + ' 2*opt')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
    

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
    

def draw(L_nbTaches, L_time,xlabel='Nombre de taches', ylabel='Temps de calcul'):
    plt.plot(L_nbTaches, L_time)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def multipledraw(L_nbTaches, M_cpt,xlabel='Nombre de taches', ylabel='Temps de calcul',courbe_label='type'):
    i = 1
    L_label= ['',"Données non-corrélées", "Corrélation sur les durées d'éxécution", "Corrélation sur les machines"]
    for L_cpt in M_cpt:
        plt.plot(L_nbTaches, L_cpt,label=L_label[i])
        i += 1 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
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
        t1[i] = math.log(t1[i])
        t2[i] = math.log(t2[i])
    x = np.array(t1)
    y = np.array(t2)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print('slope : ', slope)
    draw(t1,t2,' Log(nombre de taches)','Log(temps de résolution)')

def build_graphe(methode,name, numMax ,nbInstances, step, xlabel='nombre de taches', ylabel='temps de calcul', courbe_label='type',*args):
    prefix = 'type'
    L = []
    M = []
    for i in range(1,4):
        data_type = prefix + (str)(i)
        L_nbTaches, L_time = mesure_time(methode, data_type, numMax, nbInstances, step,*args)
        s = name + '_' + data_type
        L.append(s)
        M.append(L_time)
        save_graphe_data(s,L_nbTaches, L_time)
    print('L : ', L_nbTaches)
    print('M: ', M)
    multipledraw(L_nbTaches, M, xlabel, ylabel, courbe_label)
    

def main():
    #test()
    #L_nbTaches, L_time = mesure_time(projet.Johnson, 'type1', 200,10,5)
    #q = verifComplexite(L_nbTaches, L_time)
    #print('q : ', q)
    #build_graphe(approche.branch_and_greed,'branch_and_greed',20,5,5,'nombre de taches', 'temps de calcul', 'type', 10)
    #build_graphe(arborescence.arborescence_mix, 'b2', 8,5,1,'nombre de taches', 'temps de calcul', 'type', bornes.borneMax)
    #graphe_approximation(projet.Johnson, "approché vs exact", 8, 5 , 1)
    #compare_methodes(arborescence.arborescence_mix, arborescence.arborescence_resolve, 'initialisation', 'sans initialisation',7,5,1)
    #compare_node(arborescence.get_noeud_explore, arborescence.get_noeud_explore_b2, 'borne b1', 'borne b2',7,5,1)
    #L_nbTaches, L_time = mesure_time(projet.Johnson, 'type3', 200, 10, 5)
    #save_graphe_data('Johnson_type3', L_nbTaches, L_time)
    #L_nbTaches, L_time = mesure_time(arborescence.arborescence_resolve, 'type3', 5, 5, 1)
    #save_graphe_data('exacte_type3_b1', L_nbTaches, L_time)
    #L_nbTaches, L_time = mesure_time(arborescence.arborescence_mix, 'type3', 9, 5, 1)
    #save_graphe_data('mix_type3_b1', L_nbTaches, L_time)
    #draw(L_nbTaches, L_time)
    #print('L_nbTaches : ', L_nbTaches)
    #print('L_time : ', L_time)
    L_nbTaches, M = read_graphe_file('exacte_type1_b1','exacte_type2_b1', 'exacte_type3_b1')
    multipledraw(L_nbTaches, M, 'Nombre de taches','Temps de calcul', 'methode')
    #draw(L_nbTaches, M)
    #print(M)
    #L_nbTaches, L_cpt = mesure_node(arborescence.get_noeud_explore, 'type3', 7, 5, 1)
    #print('L_nbTaches : ', L_nbTaches)
    #print('L_cpt : ', L_cpt)
    #save_graphe_data('node_type3_b1', L_nbTaches, L_cpt)
    #draw(L_nbTaches, L_cpt,'nombre de taches','nombre de noeuds')
    

main()
