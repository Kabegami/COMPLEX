# coding: utf-8

import numpy as np
import random 

# --------------------------------------------
#              CLASS
# --------------------------------------------

class Machine(object):
    def __init__(self, P, nom='default'):
        """ P : ordonnancement """
        self.M_input = []
        self.M_output = []
        self.P = P
        self.nom = nom
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
            self.cpt_actionEnCours = 0
            self.M_input.remove(self.actionEnCours)
            self.P.remove(self.actionEnCours)

    def step(self):
        #si il y a une action en cours
        if self.actionEnCours is None:
            self.pick_tache()
        else:
            self.cpt_actionEnCours += 1
            if self.cpt_actionEnCours >= self.M[self.actionEnCours]:
                self.M_output.append(self.actionEnCours)
                self.pick_tache()
                    
    def affiche(self):
        print('--------------------------------')
        print('Machine', self.nom)
        print('Input : ' , self.M_input)
        print('Output : ', self.M_output)
        print('action en cours : ', self.actionEnCours)
        print('cpt action en cours : ', self.cpt_actionEnCours)
        print('vecteur valeur : ', self.M)
        print('--------------------------------')

class Circuit2M(object):
    def __init__(self, P, M):
        """ P : ordonnancement, M : matrice des machines/taches """
        self.P = P
        self.MA = Machine(P[::],'A')
        self.MB = Machine(P[::],'B')
        #on atribut les vecteur colonnes aux machines
        self.MA.M = M[0,:]
        self.MB.M = M[1,:]

        self.MA.M_input = P[::]
        #on fait les branchements de machine en machines
        self.MB.M_input = self.MA.M_output

    def step(self):
        self.MA.step()
        self.MB.step()

    def affiche_all(self, t=-1):
        if t != -1:
            print('Circuit t :', t)
        else:
            print('Circuit : ')
        print('================================')
        self.MA.affiche()
        self.MB.affiche()
        print('=================================')

    def resolve(self,v=False):
        time = 0
        #tant que la machine C n'a pas finit toutes ses taches
        while len(self.MB.M_output) != len(self.P):
            self.step()
            if v:
                self.affiche_all(time)
            time += 1
        #on retourne time - 1 car on veut le nombre de tour et non pas l'intervale entre debut et fin qui est nbtour + 1
        return time - 1
        
class Circuit(object):
    def __init__(self, P, M):
        """ P : ordonnancement, M : matrice des machines/taches """
        self.P = P
        self.MA = Machine(P[::],'A')
        self.MB = Machine(P[::],'B')
        self.MC = Machine(P[::],'C')
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

    def affiche_all(self, t=-1):
        if t != -1:
            print('Circuit t :', t)
        else:
            print('Circuit : ')
        print('================================')
        self.MA.affiche()
        self.MB.affiche()
        self.MC.affiche()
        print('=================================')

    def resolve(self,v=False):
        time = 0
        #tant que la machine C n'a pas finit toutes ses taches
        while len(self.MC.M_output) != len(self.P):
            self.step()
            if v:
                self.affiche_all(time)
            time += 1
        #on retourne time - 1 car on veut le nombre de tour et non pas l'intervale entre debut et fin qui est nbtour + 1
        return time - 1
        
