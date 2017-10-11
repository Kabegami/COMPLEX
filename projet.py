# coding: utf-8

import numpy as np
import random 

def read_file(fichier):
    f = open(fichier, 'r')
    matrice = []
    for line in f:
        matrice.append([float(x) for x in line.split(' ')])
    f.close()
    return matrice[0], matrice[1:]

def Johnson(M):
    """ array(int) -> L 
    prend LA, LB sous forme d'array"""
    G = []
    D = []
    t = M.shape
    print(t)
    for i in range(t[0]*t[1]):
        d = np.unravel_index(M.argmin(), M.shape)
        M[d[0]][d[1]] = np.inf
        if d[0] == 0:
            #appartient A
            G.append(d[1])
        else:
            D.append(d[1])
    return G,D

def C():
    q = list(range(8)):
    r = random.shuffle(q)
    return r

def temps_total(L1, L2, L3):
     #idealement c est des files
     #A chaque unite de temps, les machines regardent si il peuvent faire une action, si elle ne sont pas en travail.
     #on choisit les action par ordre de preference et selon les action possible ( pour C il faut que l'action passe par A et B
    

def main():
    t1, t2 = read_file('test.txt')
    nbTaches = t1[0]
    AB= np.array(t2[:-1])
    print(AB)
    L1, L2  = Johnson(AB)
    L3 = C()
    
    print(L2)
    
    
main()
