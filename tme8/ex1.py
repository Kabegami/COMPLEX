#coding: utf-8

import random
import numpy as np
import pdb

def diago(A, i,j):
    n,m = A.shape
    d = []
    starti = i
    startj = j
    while starti < n - 1  and startj > 0:
        starti += 1
        startj -= 1
    #print('starti : ', starti)
    #print('startj : ', startj)
    i = starti
    j = startj
    while j < m and i >= 0:
        #print('i : ', i)
        #print('j : ', j)
        d.append(A[i][j])
        i -= 1
        j += 1
    return d

def randomBacktrack(A):
    n,m = A.shape
    while j < n:
        #tirer une colone compatible
        r = random.randint(
        

def backtrack2(A):
    n,m = A.shape
    last= dict()
    j = 0
    while j < n:
        b = False
        for k in range(0, m):
            b = False
            dejaVu = last.get(j,[])
            if dejaVu != []:
                #netoyage
                for l in range(0, m):
                    A[l][j] = 0
            if k not in dejaVu:
                print('evaluation de k : ', k)
                A[k][j] = 1
                if not conflit(A,k,j):
                    print('pose block en i : {}, j : {}'.format(k,j))
                    b = True
                    dejaVu.append(k)
                    break
                A[k][j] = 0
        last[j] = dejaVu
        print('last[{}] : {}'.format(j, dejaVu))
        #pas de case possible backtrack
        if not b:
            print('backtrack : ', j)
            last[j] = []
            j -= 1
        else:
            print('avance')
            j +=1
    return A
            

def conflit(A, i,j):
    if sum(A[i]) > 1:
        return True
    if sum(A[:, j]) > 1:
        return True
    diag1 = np.diag(A, j - i)
#    print('diag1 : ', diag1)
    diag2 = np.diag(np.rot90(A),i)
    #if j == 3: pdb.set_trace()
    diag2 = diago(A, i, j)
    #print('diag2 : ', diag2)
    #print('i : ', i)
    #print('j : ', j)
    if sum(diag1) > 1:
        return True
    if sum(diag2) > 1:
        return True
    return False
                   
n = 8
A = np.array([[0,0,0],
              [0,1,0],
              [0,0,0]])
d = diago(A, 1,1)
print('d : ', d)
b = conflit(A, 0,2)
print('b : ', b)
M = np.zeros((n,n))
M = backtrack2(M)
print(M)


