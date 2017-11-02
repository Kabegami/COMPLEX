# coding: utf-8

import numpy as np
import bornes
import circuit
import sys
#Pour python2 utiliser Queue et non queue
version = sys.version_info[0]
if version == 2:
    import Queue as queue
else:
    import queue
import projet
import math

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
        #print('matrice : ', matrice)
        self.P = P
        self.Lrestantes = Lrestantes
        self.f_borneInf = f_borneInf
        self.borneInf = f_borneInf(P, matrice)
        self.indexFils = 0
#        print('borne inf : ', self.borneInf)
        self.borneSup = borneSup

    def expend(self,v=False):
        if self.borneInf > self.borneSup[0]:
            #on elague
            if v:
                print("==============================================")
                print('elagation')
                print('borne inf : {}'.format(self.borneInf))
                print('borne sup : {}'.format(self.borneSup))
                print("==============================================")                
            return None
        else:
            if self.indexFils < len(self.Lrestantes):
                res = self.Lrestantes[self.indexFils]
                self.indexFils += 1
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
        self.cpt = 0
        self.LNode = []
        self.LNode.append(Noeud([], matrice,taches, f_borneInf, self.borneSup))

    def expend(self,debug=False):
        node = self.LNode[-1]
        if debug:
            print('on examine le noeud ', node)
        res = node.expend(debug)
        if debug:
            print('res : ', res)
        if res == None:
            del self.LNode[-1]
        else:
            if type(res) == bool and res == True:
                #on est arriver à une feuille
                v = node.borneInf
                if len(node.P) < self.nbTaches:
                    #noeud intermedaire
                    del self.LNode[-1]
                else:
                    if debug:
                        print('--------------------------------')
                        print('on examine une feuille ')
                        print('borne inf : {}, borne sup : {}'.format(v, self.borneSup))
                        print('--------------------------------')

                    #pas nessessaire pour la borne1
                    c = circuit.Circuit(node.P, self.matrice)
                    trueValue = c.resolve()
                
                    if trueValue < self.borneSup[0]:
                        #probleme il faut prendre la vrai valeur de la solution ?
                        self.borneSup = [trueValue]
                        if debug:
                            print('la nouvelle borne sup est :', v)
                        self.bestP = node.P[::]
                        if debug: 
                            print('bestP : {}'.format(self.bestP))
                    del self.LNode[-1]
            else:
                P = (node.P)[::]
                P.append(res)
                Lrestantes = (node.Lrestantes)[::]
                Lrestantes.remove(res)
                self.cpt += 1
                new = Noeud(P, self.matrice, Lrestantes, self.f_borneInf, self.borneSup)
                if debug:
                    print("creation du noeud :", new)
                self.LNode.append(new)

    def resolve(self,v=False):
        cpt = 0
        self.cpt = 0
        while self.LNode != []:
            self.expend(v)
            if v:
                print('appel de resolve numero : {}'.format(self.cpt))
            cpt += 1
        return self.bestP, self.borneSup[0]

    def accuracy(self,debug=False):
        #A chaque hauteur de notre arbre, on a un ordonnancement de taille h.
        #La premiere case à nbTaches choix la suivant nbTaches -1 et ainsi de suite
        total = 1
        for hauteur in range(1, (int)(nbTaches)+1):
            choix = nbTaches
            n = 1
            for i in range(hauteur):
                n = n * choix
                choix -= 1
            #print('n : ', n)
            total += n
        #print('self.cpt : ', self.cpt)
        explore = (self.cpt / (1.0 * total))
        if debug:
            print("l'arbre possede {} noeuds".format(total))
            print("notre algorithme à explorer : {} noeuds".format(self.cpt))
            print("il a donc exploré : {} % de l'arbre".format((int)(explore * 100)))
        return 1 - explore

def arborescence_resolve(nbTaches, matrice, b=bornes.b1,v=False):
    print('nbTaches : ', nbTaches)
    taches = [i for i in range((int)(nbTaches))]
    tree = Arbre(taches, matrice, b)
    P, res = tree.resolve()
    tree.accuracy(v)
    return P, res

def arborescence_mix(nbTaches, matrice, b=bornes.b1,v=False):
    P1 = projet.Johnson(nbTaches, matrice)
    c = circuit.Circuit(P1, matrice)
    v = c.resolve()
    tree = Arbre(taches, matrice, b)
    tree.borneSup = [v]
    P,res = tree.resolve()
    tree.accuracy(v)
    return P, res

def combinaison(k,n):
    return (math.factorial(n) / (1.0 * math.factorial(k) * math.factorial(n -k)))
    

        

if __name__ == "__main__":
    print("***************************************************")
    print("       DEBUT DU PROGAMME")
    print("***************************************************")
    t1, t2 = read_file('Instances/exempleProf/test3.txt')
    nbTaches = t1[0]
    print(nbTaches)
    taches = [i for i in range((int)(nbTaches))]
    print('taches' ,taches)
    matrice = np.array(t2)
    print(matrice)
    #tree = Arbre(taches, matrice, bornes.b1)
    #tree = Arbre(taches, matrice, bornes.b2)
    #P, sol = tree.resolve(True)
    #print('P : ', P)
    #print('valeur de la solution optimale : ', sol)
    #c = circuit.Circuit(P, matrice)
    #res = c.resolve()
    #print('resultat du circuit : ', res)
    #accuracy = tree.accuracy(True)
    #print('accuracy : ' ,accuracy)
    P, sol = arborescence_mix(nbTaches, matrice, bornes.b2,True)
    #P,sol = arborescence_resolve(nbTaches, matrice, bornes.b1, True)
    print('P : ', P)
    print('valeur de la solution optimale : ', sol)
