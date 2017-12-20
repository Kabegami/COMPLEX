#coding: utf8

import random
import math

def pgcd(a,b):
    if a < b:
        return pgcd(b,a)
    r = a % b
    if r == 0:
        return b
    return pgcd(b,r)

def myInverse(a,N):
    for b in range(N):
        temp = (a*b) 
        if temp % N == 1:
            return b
    print("il n'existe pas d'inverse ! ")
    return None

def base2(n):
    """ base 10 -> base 2"""
    L = []
    r = float('inf')
    q = n
    while q > 0:
        r = q % 2
        L.append(r)
        q = q // 2
    L.reverse()
    return L

def expoMod(n,g,N):
    a = base2(n)
    #print('a : ', a)
    h = 1
    for i in range(len(a)-1,-1,-1):
        #print('i :',i)
        h = (h*h) % N
        if a[i] == 1:
            h = (h * g) % N
    return h

def testFermat(p, maxi=20):
    """ random """
    cpt = 0
    while cpt < maxi:
        a = random.randint(1, p-1)
        #b = expoMod(p-1, a,p)
        #print('a: ', a)
        #print('b: ',b)
        b = a**(p-1) % p
        #print('b : ',b)
        if b != 1:
            return False
        cpt += 1
    return True


def firstTest(N):
    for i in range(1,int(math.sqrt(N))):
        if N % i == 0:
            return False
    return True

def accuracy(start=1, end=10000, n=20):
    cpt = 0
    for i in range(n):
        r = random.randint(start, end)
        if testFermat(r) == firstTest(r):
            cpt += 1
    return cpt / float(n)
    
    
def test():
    assert(pgcd(2,3) == 1)
    assert(pgcd(4,2) == 2)
    assert(pgcd(9,6) == 3)

def Miller_Rabin(h,m, T):
    """ n = 1 + 2 ^ h * m, avec m impair, T : nb itérations"""
    n = 1 + (2 ** h) * m
    for i in range(1, T):
        a = random.randint(1,n)
        b = a ** m % n
        flag = False
        if b != 1 and b != (n-1):
            for j in range(1, h):
                b = b ** 2 % n
                if b == 1:
                    return False
                if b == n - 1:
                    flag = True
            if not flag:
                return False
    return True

def carmichael():
    h = 1
    m = 1
    while True:
        r = random.randint(0,1)
        if r == 0:
            h += 1
        else:
            m += 1
        yield (1 + (2 ** (h)) * m, h, m)

def test_Miller_Rabin():
    n =  1 + (2 **(2)) * 2
    b = Miller_Rabin(2,2, 20)
    C = carmichael()
    cpt = 0
    T = 50
    for i in range(T):
        v,h,m = C.next()
        print('v : ', v)
        premier = firstTest(v)
        if Miller_Rabin(h,m,20) == premier:
            cpt += 1
    print('cpt :', cpt)
    print('accuracy :', cpt / float(T))
                        
        
    

if __name__ == "__main__":
    # test()
    # b = myInverse(2,5)
    # print('b : ', b)
    # n = base2(24)
    # print('n : ', n)
    # p = expoMod(2,5,10)
    # print('p : ', p)
    # premier = testFermat(5)
    # print('test premier :', premier)
    # a = accuracy()
    # print('accuracy : ', a)
    test_Miller_Rabin()
    
