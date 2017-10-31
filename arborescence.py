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
                        print('bestP : {}'.format(self.bestP))
                    del self.LNode[-1]
            else:
                P = (node.P)[::]
                P.append(res)
                Lrestantes = (node.Lrestantes)[::]
                Lrestantes.remove(res)
                new = Noeud(P, self.matrice, Lrestantes, self.f_borneInf, self.borneSup)
                if debug:
                    print("creation du noeud :", new)
                self.LNode.append(new)

    def resolve(self,v=False):
        cpt = 0
        while self.LNode != []:
            self.expend(v)
            if v:
                print('appel de resolve numero : {}'.format(cpt))
                cpt += 1
        return self.bestP, self.borneSup[0]
        

def main():
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
    tree = Arbre(taches, matrice, bornes.b2)
    P, sol = tree.resolve(True)
    print('P : ', P)
    print('valeur de la solution optimale : ', sol)
    c = circuit.Circuit(P, matrice)
    res = c.resolve()
    print('resultat du circuit : ', res)

main()
    
    
