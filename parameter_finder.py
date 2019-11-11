# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:38:32 2019

@author: JOHNuMon
"""
from platypus import NSGAII, Problem, Real
import numpy as np
import circuit_solver as cs
import plotter as pt
import gv
import csv
import pandas as pd
def write(a,b,c):
    with open('basic_params.csv','r') as f:
        reader = csv.reader(f) #read parameter file 
        urlist=list(reader)  #converting parameter file as a list
    urlist[a][b]=c    #assigning parameter value to the list
    new = pd.DataFrame(urlist)  #rewriting the parameters back
    new.to_csv("basic_params.csv",sep=',',header=False,index=False,)   

def readus(out):
    data=np.loadtxt('ckt_output.dat')
    x=data[88,out]
    return x
            
def optimizer():
    cs.main() #calls the simulator
    pt.plot() #plots the graph after first simulation
    var=input("Do you want to optimize the circuit?\npress y to continue or n to exit program \n")
    if var=='y':
        print(" \n!!!!  optimization algorithum is running   !!!!\n")
        gv.c=1#global variable
        variables=int(input("enter no of resistors to vary"))
        for res in range(0,variables):
            Rmax=float(input("enter the range value max of resistor"))   #range of parameter search
            Rmin=float(input("enter the range value min of resistor"))
            stepvalue=float(input("enter the step with resistance value progress"))
            resistor=np.arange(Rmin,Rmax,stepvalue)
            rpos=int(input("eneter target row"))
            cpos=int(input("eneter target column"))
            resistor=list(resistor)
            resistor.append(rpos)
            resistor.append(cpos)
            gv.bigres.append(resistor)
        outpu=int(input("enter no of output parameters to vary"))
        for out in range(1,outpu+1):
            rtar_max=float(input("enter the target   value max : ")) #read the target maximum
            rtar_min=float(input("enter the target   value min : ")) #read the target minimum
            data=np.loadtxt('ckt_output.dat')
            x=data[88,out]
            outer=[]
            outer.append(rtar_max)
            outer.append(rtar_min)
            outer.append(x)
            gv.bigout.append(outer)
        for r in range(0,len(gv.bigres)):
            print (gv.bigres[r])
        for r in range(0,len(gv.bigout)):
            print (gv.bigout[r])
        return
        ga()
def ga():
    problem = Problem(2, 2)
    problem.types[:] = [Real(-2, 2),Real(-3,3)]
    problem.function = algori

    algorithm = NSGAII(problem)
    algorithm.run(10000)
    for solution in algorithm.result:
        print(solution.objectives)
    return 
def algori():
    
optimizer()    