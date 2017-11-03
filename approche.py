import random
import circuit
import projet
import random
import numpy as np
import math

class Node(object):
    def __init__(self, P,nbTaches, matrice, Lrestantes, borneEvalutation=20):
        self.P = P
        self.matrice = matrice
        self.Lrestantes = Lrestantes
        self.nbTaches = nbTaches
        self.borneEvalutation = borneEvalutation

    def getSon(self):
        L_son = []
        for val in self.Lrestantes:
            son  = self.P[::]
            son.append(val)
            L_son.append(son)
        return L_son

    def expend(self):
        nbEvalutation = min(self.borneEvalutation, math.factorial(len(self.Lrestantes)))
        #print('nbEvalutation : ', nbEvalutation)
        L_son = self.getSon()
        mini = float('inf')
        bestSon = None
        for i in range(len(L_son)):
            son = L_son[i]
            res = random_evaluation(son, self.nbTaches, self.matrice, nbEvalutation)
            if res < mini:
                mini = res
                bestSon = son
        index = len(self.P) - 1
        first_task = bestSon[index + 1]
        son_Lrestante = self.Lrestantes[::]
        son_Lrestante.remove(first_task)
        return Node(bestSon,self.nbTaches, self.matrice, son_Lrestante)
            

def random_evaluation(pi, nbTaches, matrice, nbEvalutation=10):
    taille = nbTaches - len(pi)
    mini = float('inf')
    for i in range(nbEvalutation):
        genome = pi[::]
        while len(genome) != nbTaches:
            r = random.randint(0,nbTaches-1)
            if r not in genome:
                genome.append(r)
        #print('genome : ', genome)
        c = circuit.Circuit(genome, matrice)
        res = c.resolve()
        mini = min(mini, res)
    return mini

def branch_and_greed(nbTaches, matrice,borneEvalutation=20):
    taches = [i for i in range((int)(nbTaches))]
    node = Node([],nbTaches, matrice,taches,borneEvalutation)
    while len(node.P) < nbTaches:
        node = node.expend()
    return node.P
    
        
        
if __name__ == "__main__":
    t1, t2 = projet.read_file('Instances/exempleProf/test3.txt')
    nbTaches = t1[0]
    print('nbTaches :', nbTaches)
    M = np.array(t2)
    P = branch_and_greed(nbTaches, M)
    print('P : ', P)
    c = circuit.Circuit(P, M)
    res = c.resolve()
    print('res : ' ,res)
    
