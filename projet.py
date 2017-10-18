# coding: utf-8

import numpy as np
import random 

# --------------------------------------------
#              CLASS
# --------------------------------------------

class Machine(object):
    nom = 0
    def __init__(self, P):
        """ P : ordonnancement """
        self.M_input = []
        self.M_output = []
        self.P = P
        self.nom = Machine.nom
        Machine.nom += 1
        self.actionEnCours = None
        self.cpt_actionEnCours = 0
        #M est une matrice colonne ou chaque case i correspond a la durée de la tachee i
        self.M = None

    def best_tache(self):
        if self.M_input == []:
            return None
        if self.P == []:
            return None
        for tache in self.P:
            if tache in self.M_input:
                return tache
        raise ValueError('impossible de retourner une tache', (self.M_input, self.P))

    def pick_tache(self):
        t = self.best_tache()
        self.actionEnCours = t
        if t is not None:
            self.cpt_actionEnCours = 1
            self.M_input.remove(self.actionEnCours)
            self.P.remove(self.actionEnCours)

    def step(self):
        #si il y a une action en cours
        if self.actionEnCours is None:
            self.pick_tache()
        else:
            if self.cpt_actionEnCours >= self.M[self.actionEnCours]:
                self.M_output.append(self.actionEnCours)
                self.pick_tache()
            else:
                self.cpt_actionEnCours += 1
        
    def affiche(self):
        print('--------------------------------')
        print('Machine n : ', self.nom)
        print('Input : ' , self.M_input)
        print('Output : ', self.M_output)
        print('action en cours : ', self.actionEnCours)
        print('cpt action en cours : ', self.cpt_actionEnCours)
        print('--------------------------------')
        
class Circuit(object):
    def __init__(self, P, M):
        """ P : ordonnancement, M : matrice des machines/taches """
        self.P = P
        self.MA = Machine(P[::])
        self.MB = Machine(P[::])
        self.MC = Machine(P[::])
        #on atribut les vecteur colonnes aux machines
        self.MA.M = M[0,:]
        self.MB.M = M[1,:]
        self.MC.M = M[2,:]

        self.MA.M_input = P[::]
        #on fait les branchements de machine en machines
        self.MB.M_input = self.MA.M_output
        self.MC.M_input = self.MB.M_output

    def step(self):
        self.MA.step()
        self.MB.step()
        self.MC.step()

    def affiche_all(self):
        print('Circuit : ')
        print('================================')
        self.MA.affiche()
        self.MB.affiche()
        self.MC.affiche()
        print('=================================')

    def resolve(self):
        time = 0
        #tant que la machine C n'a pas finit toutes ses taches
        while len(self.MC.M_output) != len(self.P):
            time += 1
            self.step()
            self.affiche_all()
            #import pdb; pdb.set_trace()
        return time
        
            
        


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

def retire_machine(M, machine):
    """ M : matrice, machine : machine """
    new = []
    for line in M:
        nline = []
        for i in range(len(line)):
            if i != machine:
                nline.append(line[i])
        new.append(nline)
    return np.array(new)
        

def Johnson(X, M):
    """ X : liste de tache, M:  Matrice des taches / machines """
    #il faut que M soit une matrice Machien / taches
    # probleme retourne une liste de machine au lieu dde retourner la liste des taches
    G = []
    D = []
    print(M.shape)
    while X != []:
        d = np.unravel_index(M.argmin(), M.shape)
        print('d : ', d)
        # d : (tache ,machine)
        #si c'est une tache de la machine A
        if d[0] == 0:
            #G prend la tache i
            G.append(d[1])
        #si c'est une tache de la machine B
        else:
            D.append(d[1])
        print('X : ', X)
        print(d[1])
        X.remove(d[1])
        for i in range(M.shape[0]):
            M[:, d[1]] = np.inf
        print(M)
    return G + D
        
    

def C():
    q = list(range(8))
    r = random.shuffle(q)
    return r
    

def main():
#    t1, t2 = read_file('test.txt')
#    nbTaches = t1[0]
#    AB= np.array(t2[:-1])
#    print(AB)
#    L1, L2  = Johnson(AB)
#    L3 = C()
#print(L2)
    t1, t2 = read_file('test.txt')
    nbTaches = t1[0]
    M = np.array(t2)
    #il faut créer une fonction qui retire une machine
    AB = retire_machine(M, 2)
    print(type(AB))
    print('AB : ', AB)
    X = [ i for i in range(M.shape[1]) ]
    print(X)
    P = Johnson(X, AB)
    print("P : ", P)
    solver = Circuit(P, M)
    t = solver.resolve()
    print('M : ', solver.MC.M)
    print(t)
    
    
main()
