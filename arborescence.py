# coding: utf-8

import numpy as np
import bornes
import circuit
import queue

def read_file(fichier):
    f = open(fichier, 'r')
    matrice = []
    for line in f:
        matrice.append([float(x) for x in line.split(' ')])
    f.close()
    return matrice[0], matrice[1:]

class Noeud(object):
    def __init__(self, P, matrice, Lrestantes, f_borneInf, borneSup):
        #borneSup est une liste !
        print('matrice : ', matrice)
        self.P = P
        self.Lrestantes = Lrestantes
        self.f_borneInf = f_borneInf
        self.borneInf = f_borneInf(P, matrice,True)
        self.borneSup = borneSup

    def expend(self):
        if self.borneInf > self.borneSup[0]:
            #on elague
            return None
        else:
            if self.Lrestantes != []:
                res = self.Lrestantes[0]
                del self.Lrestantes[0]
                return res
            else:
                return True

    def __str__(self):
        s = "Noeud de l'ordonancement : {}".format(self.P)
        return s


class Arbre(object):
    def __init__(self, taches, matrice, f_borneInf):
        self.matrice = matrice
        self.borneSup = [float('inf')]
        self.bestP = None
        #on garde la borne sup dans une liste car on veut un pointeur et pas une copie
        self.f_borneInf = f_borneInf
        self.taches = taches
        self.nbTaches = len(taches)
        self.LNode = []
        self.LNode.append(Noeud([], matrice,taches, f_borneInf, self.borneSup))

    def expend(self):
        node = self.LNode[-1]
        res = node.expend()
        if res == None:
            print('on supprime une feuille')
            del self.LNode[-1]
        else:
            if res == True:
                #on est arriver à une feuille
                v = node.borneInf
                if v < self.borneSup:
                    self.borneSup = [v]
                    print('la nouvelle borne sup est :', v)
                    self.bestP = node.P[::]
            else:
                P = (node.P)[::]
                P.append(res)
                Lrestantes = (node.Lrestantes)[::]
                new = Noeud(P, self.matrice, Lrestantes, self.f_borneInf, self.borneSup)
                print("creation du noeud :", new)
                Lrestantes.append(new)

    def resolve(self):
        while self.LNode != []:
            self.expend()
        return self.bestP
        

def main():
    t1, t2 = read_file('Instances/test2.txt')
    nbTaches = t1[0]
    print(nbTaches)
    taches = [i for i in range((int)(nbTaches))]
    print('taches' ,taches)
    matrice = np.array(t2)
    print(matrice)
    tree = Arbre(taches, matrice, bornes.b1)
    P = tree.resolve()
    print('P : ', P)

main()
    
    
