# coding: utf-8

import numpy as np
import circuit
import random

def read_file(fichier):
    f = open(fichier, 'r')
    matrice = []
    for line in f:
        matrice.append([float(x) for x in line.split(' ')])
    f.close()
    return matrice[0], matrice[1:]

def borneA(pi, matrice,v=False):
    """ pi : ordonnancement (liste), matrice des taches np.array"""
    #ATTENTION la matrice qu'on stoque dans les fichiers n'a pas le bon format vis à vis des données
    #m = matrice.T
    m = matrice
    if v:
        print("matrice A : ", matrice)
    machineA = matrice[0]
    if v:
        print("machineA",machineA)
    s = 0
    #s'occupe de tpiA et de SIGMA(dia) en meme tmeps
    for i in range(len(machineA)):
        s += machineA[i]

    if len(pi) == len(matrice[0]):
        #cas particulier ou pi est un ordonancement final
        return s

    mini = float("inf")
    index_mini = None
    BC = matrice[1:3]
    if v:
        print("=======================")
        print('BC : ', BC)
        print("=======================")
    for i in range(len(BC[0])):
        if i not in pi:
            mini = min(mini, BC[0][i] + BC[1][i])
    if v:
        print('plus petite somme : ', mini)
    return s + mini

def borneB(pi, matrice,v=False):
    s = 0
    c = circuit.Circuit2M(pi, matrice)
    tB = c.resolve()
    if len(pi) == len(matrice[0]):
        #cas particulier ou pi est un ordonancement final
        return tB
    borneB = 0
    tA = 0
    if v:
        print("matrice : ", matrice) 
    machineA = matrice[0]
    if v:
        print("machineA : ", machineA)
    miniA = float("inf")
    for i in range(len(machineA)):
        if i in pi:
            tA += machineA[i]
        else:
            if machineA[i] < miniA:
                miniA = machineA[i]
    s += max(tB, tA + miniA)
    machineB = matrice[1]

    for i in range(len(machineB)):
        if not(i in pi):
            s += machineB[i]

    machineC = matrice[2]
    miniC = float("inf")
    for i in range(len(machineC)):
        if not ( i in pi):
            if machineC[i] < miniC:
                miniC =machineC[i]
    s += miniC
    return s

def borneC(pi, matrice,v=False):
    s = 0
    c = circuit.Circuit(pi,matrice)
    tc = c.resolve()
    if len(pi) == len(matrice[0]):
        #cas particulier ou pi est un ordonancement final
        return tc
    #amelioration tC prime
    c = circuit.Circuit2M(pi, matrice)
    tB = c.resolve()
    if v:
        print('matrice : ', matrice)
    machineA = matrice[0]
    machineB = matrice[1]
    machineC = matrice[2]
    tA = 0
    miniB = float("inf")
    miniAB = float("inf")
    for i in range(len(machineC)):
        if i not in pi:
            s += machineC[i]
            miniB = min(miniB, machineB[i])
            miniAB = min(miniAB, machineA[i] + machineB[i])
        else:
            tA += machineA[i]
    s += max(tc, tB + miniB, tA + miniAB)
    return s

def b1(pi, matrice,v=False):
    bA = borneA(pi, matrice,v)
    bB = borneB(pi, matrice,v)
    bC = borneC(pi, matrice,v)
    return max(bA,bB,bC)

def b2k(pi, matrice,tA, k):
    s = tA
    #ajout de la tache k
    s += np.sum(matrice[:, k])
    machineA = matrice[0]
    machineC = matrice[2]
    for i in range(len(machineA)):
        if i not in pi and i != k:
            if machineA[i] < machineC[i]:
                s += machineA[i]
            else:
                s +=machineC[i]
    return s

def b2(pi, matrice,v=False):
    #la borne 2 est trop optimiste du coup quand on est dans une feuille, on a une mauvaise estimation
    s = 0
    machineA = matrice[0]
    machineB = matrice[1]
    machineC = matrice[2]
    tA = 0
    piPrime = []
    for i in range(len(machineA)):
        if i in pi:
          tA += machineA[i]
        else:
            piPrime.append(i)
    s += tA
    #si il n'y a pas de piPrime
    if len(pi) == len(machineA):
        return s
    #on selectionne k n'appartenant pas a P
    maxi = -1 * float('inf')
    for k in piPrime:
        maxi = max(maxi, b2k(pi, matrice, tA, k))
    if v:
        print('taille : ', len(machineA) -1)
        print('k : ', k)
        print('vecteur k : ', matrice[:,k])
        print('maxi : ', maxi)
    s = maxi
    return s

def b3k(pi, matrice, tB, k, v=False):
    s = tB
    machineB = matrice[1]
    machineC = matrice[2]
    if v:
        print('k : ', k)
        print('machineB : ', machineB)
    s += machineB[k] + machineC[k]
    for i in range(len(machineB)):
        if i not in pi and i != k:
            if machineB[i] < machineC[i]:
                s += machineB[i]
            else:
                s +=machineC[i]
    return s

def b3(pi, matrice,v=False):
    c = circuit.Circuit2M(pi, matrice)
    tB = c.resolve()
    maxi = -1 * float('inf')
    if len(pi) == len(matrice[1]):
        return tB
    for i in range(len(matrice[0])):
        if i not in pi:
            maxi = max(maxi, b3k(pi, matrice, tB, i, v))
    s = maxi
    return s

def borneMax(pi, matrice):
    return max(b1(pi, matrice), b2(pi,matrice), b3(pi, matrice))

def main():
    t1, t2 = read_file('Instances/exempleProf/test3.txt')
    nbTaches = t1[0]
    print(nbTaches)
    matrice = np.array(t2)
    m = matrice.T
    ba = borneA([0],matrice)
    bB = borneB([0],matrice)
    bC = borneC([0],matrice)
    print('ba : ', ba)
    print('bB : ', bB)
    print('bC : ', bC)
    borne1 = b1([0], matrice)
    print('borne 1 :' , borne1)
    borne2 = b2([0], matrice)
    print('borne2 : ', borne2)
    borne3 = b3([0], matrice)
    print('borne3 : ', borne3)

#main()
