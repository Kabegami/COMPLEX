# coding: utf-8

import random
import math
import numpy as np

def genere1(nbTaches, ai=1, bi=100):
    mat = []
    for machines in range(3):
        LTaches = []
        for taches in range(nbTaches):
            r = random.random() * (bi - ai) + ai
            LTaches.append(r)
        mat.append(LTaches)
    return (nbTaches, mat)

def genere2(nbTaches):
    mat = []
    for machines in range(3):
        L = []
        for taches in range(nbTaches):
            ri = random.random()*4
            ai = 20*ri
            bi = 20*ri +20
            t = random.random()*(bi-ai) + ai
            L.append(t)
        mat.append(L)
    return (nbTaches, mat)

def genere3(nbTaches):
    mat = []
    for x in range(1,4):
        #print('x : ', x)
        L = []
        for taches in range(nbTaches):
            ai = 15*(x - 1) + 1
            bi = 15*(x - 1) + 100
            r =  random.random()*(bi-ai) + ai
            L.append(r)
        mat.append(L)
    return (nbTaches, mat)

def test_genere3(nbTaches=8):
    #on verifie que la moyenne(A) < moyenne(B) < moyenne(C) de maière générale
    nbTaches, mat = genere3(nbTaches)
    matrice = np.array(mat)
    for line in mat:
        print('moyenne :', np.average(line))
    
    
def instance_to_string(instance):
    """ instance : tuple (nbTaches, matrice)"""
    nbTaches, matrice = instance
    s = ""
    s += (str)(nbTaches) + '\n'
    for line in matrice:
        l = ''
        for tache in line:
            l += (str)(tache) + ' '
        s += l[:-1] + '\n'
    return s[:-1]

def save(fichier, data):
    """ fichier : nom du fichier, data : tuple (nbTaches, matrice) """
    f = open(fichier, 'w')
    instance = instance_to_string(data)
    f.write(instance)
    f.close()

def createInstance(fichier,fGeneration=genere1, save=True, nbInstance=10, nbTaches=8):
    L_global_mat = []
    for i in range(nbInstance):
        n, matrice = fGeneration(nbInstance)
        L_global_mat.append(matrice)

    global_mat = np.array(L_global_mat)
    #print('global mat : ', global_mat)
    #puis on parcours la matrice global
    mat = global_mat[0].copy()
    for i in range(1, nbInstance):
        mat2 = global_mat[i]
        mat += mat2
    mat /= (1.0 * nbInstance)
    if save:
        save(fichier, (nbTaches, mat))
    return mat

        

def main():
    nbTaches = 8
    t = genere1(nbTaches)
    s = instance_to_string(t)
    t2 = genere2(nbTaches)
    s2 = instance_to_string(t2)
    t3 = genere3(8)
    s3 = instance_to_string(t3)
    mat = np.array(t3[1])
    print(s3)
    g = createInstance('',genere3,False,10,8)
    print(g)
#   print(s2)
    #print(s)
    #save('my_data_m1', t)

main()


