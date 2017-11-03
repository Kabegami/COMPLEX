# coding: utf-8

import random
import math
import numpy as np
import os


def genere1(nbTaches, ai=1, bi=100):
    """Génération de données non-corrélées (dites de Taillard):
    Les temps d'exécution pour chaque tâche sur chaque machine sont des entiers 
    tirés uniformément dans l'intervale spécifié par les bornes données en 
    argument.
    
    Args:
        nbTaches (int): nombre de tâches générées.
        ai (int): borne inférieure pour le tirage du temps mis par une tâche.
            (Doit être supérieur à 0, valeur par défaut=1).
        bi (int): borne supérieure pour le tirage du temps miss par une tâche.
            (Doit être supérieur à `ai`, valeur par défaut=100).

    Returns:
        nbTaches (int)
        mat (int matrix): matrice des temps d'exécution pour chaque tâche sur
            chaque machine. 
    """
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
    """Génération de données corrélées sur les temps d'exécution:
    Les temps d'exécution générés sont des entiers tirés dans l'intervale 
    [ai, bi] avec:
    ai = 20*ri
    bi = 20*ri + 20
    ri tiré aléatoirement dans [0, 1, 2, 3, 4].

    Args:
        nbTaches (int): nombre de tâches générées.

    Returns:
        nbTaches (int)
        mat (int matrix): matrice des temps d'exécution pour chaque tâche sur
            chaque machine.
    """
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
    """Génération de données corrélées sur les machines.

    Args:
        nbTaches (int): nombre de tâches générées.

    Returns:
        nbTaches (int)
        mat (int matrix): matrice des temps d'exécution pour chaque tâche sur
            chaque machine.
    """
    mat = []
    for x in range(1,4):
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
    # on verifie que la moyenne(A) < moyenne(B) < moyenne(C) de maière générale
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

def createInstance(dossier, fGeneration, nbTaches, nbInstance, saveInstance=True):
    prefix = dossier + '/' + 'test'
    for i in range(nbInstance):
        filename = prefix + (str)(i)
        n, matrice = fGeneration(nbTaches)
        if saveInstance:
            save(filename, (nbTaches, matrice))
    

def creer_jeu_de_test(dossier, fGeneration, nbTest, nbInstance=10, step=5):
    print("===============================================")
    print("Debut de la creation de jeu de test")
    prefix = dossier
    nbTaches = step
    for i in range(nbTest):
        dirname = prefix + 'instances' + (str)(nbTaches)
        #creation du dossier si il n'existe pas
        if not(os.path.exists(dirname)):
            os.mkdir(dirname)
        createInstance(dirname, fGeneration, nbTaches, nbInstance, True)
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
    #g = createInstance('',genere1,False,10,8)
    #print(g)
    #creer_jeu_de_test('Instances/type3/', genere3, 40,  10)
    #create_dataSet(80,10,5)
    create_dataSet(20,10,1)
#   print(s2)
    #print(s)
    #save('my_data_m1', t)

    
if __name__ == "__main__":
   main()

# main()

