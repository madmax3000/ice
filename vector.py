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
    f=pd.read_csv(gf.diagramarray[flno-1],header=None,index_col=False)
    ele=f.iloc[p[0],p[1]]
    return ele
#-----------------------------------------------------------------
def splitString(str):
    alpha = ""
    num = ""
    special = ""
    for i in range(len(str)):
        if (str[i].isdigit()):
            num = num + str[i]
        elif ((str[i] >= 'A' and str[i] <= 'Z') or
              (str[i] >= 'a' and str[i] <= 'z')):
            alpha += str[i]
        else:
            special += str[i]
    return [alpha,num]
#-----------------------------------------------------------------------
def indexfinder(f):
    apna = splitString(f.upper())
    r=int(apna[1])-1  #now support added for
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
        "Z":25,
        "AA": 26,
        "AB": 27,
        "AC": 28,
        "AD": 29,
        "AE": 30,
        "AF": 31,
        "AG": 32,
        "AH": 33,
        "AI": 34,
        "AJ": 35,
        "AK": 36,
        "AL": 37,
        "AM": 38,
        "AN": 39,
        "AO": 40,
        "AP": 41,
        "AQ": 42,
        "AR": 43,
        "AS": 44,
        "AT": 45,
        "AU": 46,
        "AV": 47,
        "AW": 48,
        "AX": 49,
        "AY": 50,
        "AZ": 51
        }
    posl=[]
    for x in alpha:# a permanant fix for this index long issue is required
        if (apna[0] == x):
            c = alpha[x]
            posl.append(r)
            posl.append(c)
            return posl
        
def writer_of_vector(address,element_to_write,fileno):
    abe=indexfinder(address)
    a=abe[0]
    b=abe[1]
    c=element_to_write
    with open(gf.diagramarray[int(fileno)-1], 'r') as f:
        readprofile = csv.reader(f)  # read parameter file
        urlize = list(readprofile)  # converting parameter file as a list
    urlize[a][b] = c  # assigning parameter value to the list
    new = pd.DataFrame(urlize)  # rewriting the parameters back
    new.to_csv(gf.diagramarray[int(fileno)-1], sep=',', header=False, index=False, )
    #for  fix of writer
    return




