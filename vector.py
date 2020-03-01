# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:50:33 2020

@author: JENSON JOSE
"""
import gv
import pandas as pd
import csv
import globalfile as gf
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

# reader to find the element from its location
def reader(flno,p):
    f=pd.read_csv(gf.diagramarray[flno],header=None,index_col=False)
    ele=f.iloc[p[0],p[1]]
    return ele

def indexfinder(f):
    posl=[]
    b=list(f)
    k=int(b[1])
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
        if (b[0] == x):
            c = alpha[x]
            posl.append(r)
            posl.append(c)
            return posl
        
def writer_of_vector(address,element_to_write,fileno):
    abe=indexfinder(address)
    a=abe[0]
    b=abe[1]
    c=element_to_write
    with open(gf.diagramarray[fileno], 'r') as f:
        readprofile = csv.reader(f)  # read parameter file
        urlize = list(readprofile)  # converting parameter file as a list
    urlize[a][b] = c  # assigning parameter value to the list
    new = pd.DataFrame(urlize)  # rewriting the parameters back
    new.to_csv(gf.diagramarray[fileno], sep=',', header=False, index=False, )
    print("writing is working") #for debug
    return
    '''
    f=pd.read_csv(gv.cktfile,header=None,index_col=False)
    f.iloc[a[0],a[1]]=element_to_write
    f.to_csv(gv.cktfile,sep=',',header=False,index=False,)
    return
    '''
