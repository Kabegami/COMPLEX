#encodage utf8

import numpy as np
import circuit

def read_file(fichier):
    f = open(fichier, 'r')
    matrice = []
    for line in f:
        matrice.append([float(x) for x in line.split(' ')])
    f.close()
    return matrice[0], matrice[1:]

def borneA(pi, matrice):
    """ pi : ordonnancement (liste), matrice des taches np.array"""
    #ATTENTION la matrice qu'on stoque dans les fichiers n'a pas le bon format vis à vis des données
    #m = matrice.T
    m = matrice
    print(m)
    machineA = m[0,:]
    #print("machineA",machineA)
    s = 0
    for i in range(len(machineA)):
        if i in pi:
            s += machineA[i]
    

    mini = float("inf")
    index_mini = None
    BC = m[:,1:]
    for i in range(len(BC)):
        if (i+1) not in pi:
            line = BC[i]
            print('line :', line)
            v = np.sum(line)
            print('v : ', v)
            if v < mini:
                mini = v
    return s + mini

def borneB(pi, matrice):
    s = 0
    c = circuit.Circuit2M(pi, matrice)
    tB = c.resolve()
    borneB = 0
    tA = 0
    print("matrice : ", matrice)
    m = matrice.T
    print("m :", m) 
    machineA = m[0]
    miniA = float("inf")
    for i in range(len(machineA)):
        if i in pi:
            tA += machineA[i]
        else:
            if machineA[i] < miniA:
                miniA = machineA[i]
    s += max(tB, tA + miniA)
    machineB = m[1]

    for i in range(len(machineB)):
        if not(i in pi):
            s += machineB[i]

    machineC = m[2]
    miniC = float("inf")
    for i in range(len(machineC)):
        if not ( i in pi):
            if machineC[i] < miniC:
                miniC =machineC[i]
    s += miniC
    return s
    

def main():
    t1, t2 = read_file('Instances/test2.txt')
    nbTaches = t1[0]
    print(nbTaches)
    matrice = np.array(t2)
    m = matrice.T
    ba = borneA([0],m)
    bB = borneB([0],matrice)
    print('ba : ', ba)
    print('bB : ', bB)

main()
