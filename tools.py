# coding: utf-8

import random
import math
import numpy as np

def genere1(nbTaches, ai=1, bi=100):
    mat = []
    for machines in range(3):
        LTaches = []
        for taches in range(nbTaches):
            #r = random.random() * (bi - ai) + ai
            r = random.randint(ai, bi)
            LTaches.append(r)
        mat.append(LTaches)
    return (nbTaches, mat)

def genere2(nbTaches):
    mat = []
    for machines in range(3):
        L = []
        for taches in range(nbTaches):
            ri = random.randint(0,4)
            ai = 20*ri
            bi = 20*ri +20
            #t = random.random()*(bi-ai) + ai
            t = random.randint(ai, bi)
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
            #r =  random.random()*(bi-ai) + ai
            r = random.randint(ai,bi)
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

def createInstance(fichier,fGeneration=genere1, saveInstance=True,nbTaches=8, nbInstance=10):
    L_global_mat = []
    for i in range(nbInstance):
        n, matrice = fGeneration(nbTaches)
        L_global_mat.append(matrice)

    global_mat = np.array(L_global_mat)
    #puis on parcours la matrice global
    mat = global_mat[0].copy()
    for i in range(1, nbInstance):
        mat2 = global_mat[i]
        mat += mat2
    res = mat // (1.0 * nbInstance)
    #mat /= (1.0 * nbInstance)
    res = res.astype(int)
#    print('res : ', res)
#    print('type matrice : ', res.dtype)
    if saveInstance:
        save(fichier, (nbTaches, res))
    return res

def creer_jeu_de_test(dossier, fGeneration, nbTest, nbInstance=10, step=5):
    print("===============================================")
    print("Debut de la creation de jeu de test")
    prefix = dossier
    nbTaches = step
    for i in range(nbTest):
        filename = prefix + 'instances' + (str)(nbTaches)
        createInstance(filename, fGeneration,True, nbTaches, nbInstance)
        nbTaches += step
    print("Fin de la creation des tests")
    print("===============================================")

def create_dataSet(nbTest,nbInstance,step=5):
    creer_jeu_de_test('Instances/type1/', genere1, nbTest, nbInstance,step)
    creer_jeu_de_test('Instances/type2/', genere2, nbTest, nbInstance,step)
    creer_jeu_de_test('Instances/type3/', genere3, nbTest, nbInstance,step)
        
    

def main():
    nbTaches = 8
    t = genere1(nbTaches)
    s = instance_to_string(t)
    t2 = genere2(nbTaches)
    s2 = instance_to_string(t2)
    t3 = genere3(8)
    s3 = instance_to_string(t3)
    mat = np.array(t3[1])
    print('s : ', s)
    print('s2 : ', s2)
    print('s3 : ', s3)
    g = createInstance('',genere1,False,10,8)
    print(g)
    #creer_jeu_de_test('Instances/type3/', genere3, 40,  10)
    create_dataSet(40,10)
#   print(s2)
    #print(s)
    #save('my_data_m1', t)

main()


