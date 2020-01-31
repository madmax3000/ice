# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:50:33 2020

@author: JENSON JOSE
"""
import mainframe as main
import pandas as pd
# Python function to print permutations of a given list 

def permutation(lst): 

  

    # If lst is empty then there are no permutations 

    if len(lst) == 0: 

        return [] 

  

    # If there is only one element in lst then, only 

    # one permuatation is possible 

    if len(lst) == 1: 

        return [lst] 

  

    # Find the permutations for lst if there are 

    # more than 1 characters 

  

    l = [] # empty list that will store current permutation 

  

    # Iterate the input(lst) and calculate the permutation 

    for i in range(len(lst)): 

       m = lst[i] 


       # Extract lst[i] or m from the list.  remLst is 

       # remaining list 

       remLst = lst[:i] + lst[i+1:] 
     

  

       # Generating all permutations where m is first 

       # element 

       for p in permutation(remLst): 

           l.append([m] + p) 
       

    return l 

  

  
# Driver program to test above function 


def reader(p):
    f=pd.read_csv("buck_ckt.csv",header=None,index_col=False)
    ele=f.iloc[p[0],p[1]]
    return ele

def indexfinder(f):
    posl=[]
    b=list(f)
    k=int(b[0])
    r=k-1
    alpha={ "A":0,
        "B":1,
        "C":2,
        "D":3,
        "E":4,
        "F":5,
        "G":6,
        "H":7,
        "I":8,
        "J":9,
        "K":10,
        "L":11,
        "M":12,
        "N":13,
        "O":14,
        "P":15,
        "Q":16,
        "R":17,
        "S":18,
        "T":19,
        "U":20,
        "V":21,
        "W":22,
        "X":23,
        "Y":24,
        "Z":25
        }
    for x in alpha:
        if (b[1] == x):
            c = alpha[x]
            posl.append(r)
            posl.append(c)
            return posl
        
def write(address,element_to_write):
    a=indexfinder(address)
    f=pd.read_csv("buck_ckt.csv",header=None,index_col=False)
    f.iloc[a[0],a[1]]=element_to_write
    f.to_csv("buck_ckt.csv",sep=',',header=False,index=False,) 
    return

def vctmain():

    n=int(input("enter the no of elements to change"))
    addr=[]
    elm=[]
    superlist=[]

    for i in range(0,n):
        y=input("enter the positions")
        addr.append(y)
        print(addr)
        m=indexfinder(addr[i])
        print(m)
        elm.append((reader(m)))
    superlist=permutation(elm)
    print(elm)
    print(superlist)

    for i in range(len(superlist)):
        for j in range(len(addr)):
            write(addr[j],superlist[i][j])
            main.initalization()
            main.ga()
            return



              
