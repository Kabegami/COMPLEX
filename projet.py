# coding: utf-8

import numpy as np
import circuit
import random 

# --------------------------------------------
#              FUNCTION
# --------------------------------------------

def read_file(fichier):
    f = open(fichier, 'r')
    matrice = []
    for line in f:
        matrice.append([float(x) for x in line.split(' ')])
    f.close()
    return matrice[0], matrice[1:]

def retire_tache(M, tache):
    """ M : matrice, t : tache """
    new = []
    for i in range(len(M)):
        if i != tache:
            #a priori faire une copie n'est pas necessaire
            new.append(M[i])
    return np.array(new)

def retire_machine(M, machine=-1):
    """ M : matrice, machine : machine """
    return M[:-1,:]
        

def Johnson(X, matrice,v=False):
    """ X : liste de tache, M:  Matrice des taches / machines """
    #il faut que M soit une matrice Machien / taches
    # probleme retourne une liste de machine au lieu dde retourner la liste des taches
    G = []
    D = []
    M = matrice.copy()
    if v:
        print('m shape : ', M.shape)
    while X != []:
        d = np.unravel_index(M.argmin(), M.shape)
        if v:
            print('d : ', d)
        #si c'est une tache de la machine A
        if d[0] == 0:
            #G prend la tache i
            G.append(d[1])
        #si c'est une tache de la machine B
        else:
            D.append(d[1])
        if v:
            print('X : ', X)
            print(d[1])
        X.remove(d[1])
        for i in range(M.shape[0]):
            M[:, d[1]] = np.inf
        if v:
            print(M)
    return G + D
        
    

def C():
    q = list(range(8))
    r = random.shuffle(q)
    return r
    

if __name__ == "__main__":
    t1, t2 = read_file('Instances/exempleProf/test2.txt')
    nbTaches = t1[0]
    M = np.array(t2)
    #il faut créer une fonction qui retire une machine
    AB = retire_machine(M)
    print('AB : ', AB)
    X = [ i for i in range(M.shape[1]) ]
    P = Johnson(X, AB)
    print("P : ", P)
    solver = circuit.Circuit(P, M)
    t = solver.resolve(True)
    print('M : ', solver.MC.M)
    print(t)
    
    
main()
