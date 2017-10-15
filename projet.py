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

def retire_tache(M, tache):
    """ M : matrice, t : tache """
    new = []
    for i in range(len(M)):
        if i != tache:
            #a priori faire une copie n'est pas necessaire
            new.append(M[i])
    return np.array(new)

def retire_machine(M, machine):
    """ M : matrice, machine : machine """
    new = []
    for line in M:
        nline = []
        for i in range(len(line)):
            if i != machine:
                nline.append(line[i])
        new.append(nline)
    return np.array(new)
        

def Johnson2(X, M):
    """ X : liste de tache, M:  Matrice des taches / machines """
    #il faut que M soit une matrice Machien / taches
    G = []
    D = []
    while X != []:
        d = np.unravel_index(M.argmin(), M.shape)
        print('d : ', d)
        print(M.shape)
        #si c'est une tache de la machine A
        if d[0] == 0:
            #G prend la tache i
            G.append(d[1])
        #si c'est une tache de la machine B
        else:
            D.append(d[1])
        X.remove(d[1])
        # !!! Attention on perd les index de tache de cette façon ... !!!
        for i in range(M.shape[1]):
            M[d[1]] = np.inf
        print(M)
    return G + D
        
    

def C():
    q = list(range(8))
    r = random.shuffle(q)
    return r

def temps_total(L1, L2, L3):
     #idealement c est des files
     #A chaque unite de temps, les machines regardent si il peuvent faire une action, si elle ne sont pas en travail.
     #on choisit les action par ordre de preference et selon les action possible ( pour C il faut que l'action passe par A et B
    pass
    

def main():
#    t1, t2 = read_file('test.txt')
#    nbTaches = t1[0]
#    AB= np.array(t2[:-1])
#    print(AB)
#    L1, L2  = Johnson(AB)
#    L3 = C()
#print(L2)
    t1, t2 = read_file('test2.txt')
    nbTaches = t1[0]
    M = np.array(t2)
    #il faut créer une fonction qui retire une machine
    AB = retire_machine(M, 2)
    print(type(AB))
    print('AB : ', AB)
    X = [ i for i in range(len(M)) ]
    print(X)
    L = Johnson2(X, AB)
    print(L)
    
    
main()
