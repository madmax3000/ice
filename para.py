# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:38:32 2019

@author: JOHNuMon
"""

from platypus import OMOPSO, Problem, Real,nondominated,InjectedPopulation,Solution
from function import avg,ripple,rms,signalselector,thd
import numpy as np
import circuit_solver as cs
import plotter as pt
import gv
import csv
import statistics
import pandas as pd
gv.counter=0
def write(a,b,c):
    with open('buck_ckt_params.csv','r') as f:
        reader = csv.reader(f) #read parameter file 
        urlist=list(reader)  #converting parameter file as a list
    urlist[a][b]=c    #assigning parameter value to the list
    new = pd.DataFrame(urlist)  #rewriting the parameters back
    new.to_csv("buck_ckt_params.csv",sep=',',header=False,index=False,)   

def readus_avg(out):
    data=np.loadtxt('ckt_output2.dat')
    x=data[:,out]#read data file
    y=signalselector(x)
    m=avg(y)
    return m
def readus_ripple(out):
    data=np.loadtxt('ckt_output2.dat')
    x=data[:,out]#read data file
    y=signalselector(x)
    n=ripple(y)
    return n
def readus_rms(out):
    data=np.loadtxt('ckt_output2.dat')
    x=data[:,out]#read data file
    y=signalselector(x)
    p=rms(y)
    return p
def readus_thd(out):
    data=np.loadtxt('ckt_output2.dat')
    x=data[:,out]#read data file
    y=signalselector(x)
    th=thd(y)
    return th
    
    
def evaluator(vars):
    gv.counter=gv.counter+1
    print("the counter value is ",gv.counter)
    for m in range(0,len(gv.bigres)):
        #simin.append(vars[m])
        #if gv.bigres[m][4]==1:
        a=gv.bigres[m][2]#write parameters to the circuit para meters
        b=gv.bigres[m][3]
        write(a,b,vars[m])#vars is the output from the prediction of genetic algorithm
        '''
        else:
            gv.d=vars[m]
            print("duty ratio now is ",gv.d)
        '''
    cs.main()
    for n in range(0,len(gv.bigout)):
        if gv.bigout[n][3]== 1.0 :#read circuit output parameters
            lol=gv.bigout[n][4]
            x=readus_avg(lol-1)
            gv.bigout[n][2]=x
            #print("this is avg value",x)
        else:
            lol=gv.bigout[n][4]
            x=readus_ripple(lol-1)
            gv.bigout[n][2]=x
            #print("this is ripple",x)
    '''
    count=0
    for n in range(0,len(gv.bigout)):
        k=gv.bigout[n][0]
        l=gv.bigout[n][1]
        j=gv.bigout[n][3]#comparing each output
        if(k>=j and l<=j):
            count=count+1
    if(count==len(gv.bigout)):
        for m in range(0,len(gv.bigres)):
            print("the value of element",m ,"is",vars[m])
            exit#time to exit code
    else:
        '''
    lis=[]
    for n in range(0,len(gv.bigout)):
        a=(gv.bigout[n][2]-gv.bigout[n][3])**2
        lis.append(a) #returns result out put to genetic algorithm
    
    return lis
            
        

def optimizer():
    #trial run
    cs.main() #calls the simulator
    pt.plot() #plots the graph after first simulation
    #m=readus_ripple(2)
    n=readus_avg(3)
    #p=readus_rms(3)
    #th=readus_thd(4)
    #print(m,n,p,th)
    print("the avg",n)
    #trial run ends here
    var=input("Do you want to optimize the circuit?\npress y to continue or n to exit program \n")
    if var=='y':
        print(" \n!!!!  optimization algorithum is running   !!!!\n")
        gv.c=1    #global variable
        #optimizer  input intialisation
        variables=int(input("enter no of elements to vary"))
        for res in range(0,variables):
            resistor=[]
            Rmax=float(input("enter the range value max of element:"))   #range of parameter search
            resistor.append(Rmax) #read max value
            Rmin=float(input("enter the range value min of elemenet:"))
            resistor.append(Rmin) #read min value
            rpos=int(input("eneter target row"))
            resistor.append(rpos)  #read row
            cpos=3
            resistor.append(cpos)  #read column
            gv.bigres.append(resistor)   #combine to a large matrix global matrix in gv.py
            for r in range(0,len(gv.bigres)):
                print (gv.bigres[r])
        outpu=int(input("enter no of output parameters to optimize"))
        for out in range(1,outpu+1):
            outer=[]
            rtar_max=float(input("enter the target   value max : ")) #read the target maximum
            outer.append(rtar_max)
            rtar_min=float(input("enter the target   value min : ")) #read the target minimum
            outer.append(rtar_min)
            outermean=statistics.mean(outer)
            outer.append(outermean)
            rval=float(input("1 for avg,2 for ripple : "))#take mean set as an target value
            #data=np.loadtxt('ckt_output2.dat') #read data from output
            #x=data[8,out] #assignn value to a variable
            #outer.append(x)
            outer.append(rval)
            pos=int(input("enter output meter no in output file "))
            outer.append(pos)
            gv.bigout.append(outer) #update to a global matix
            for r in range(0,len(gv.bigout)):
                print (gv.bigout[r])
        ga(variables,outpu) #call genetic algorithm
        return
def ga(variables,outpu):
    problem = Problem(variables,outpu) #specify the no of objectives and inputs
    for i in range(0,len(gv.bigres)):
        for j in range(0,len(gv.bigres[i])-2):
            problem.types[i:i+1] = [Real(gv.bigres[i][j],gv.bigres[i][j+1])] #loop to intialise the limkits
    
    problem.function = evaluator#call the simulator
    v_population_size = 10
    init_pop = [Solution(problem) for i in range(v_population_size)]
    pop_indiv = [[x.rand() for x in problem.types] for i in range(v_population_size)]

    for i in range(v_population_size):
        init_pop[i].variables = pop_indiv[i]
	
    algorithm = OMOPSO(problem,10, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    algorithm.run(200)   
    feasible_solutions = [s for s in algorithm.result if s.feasible] 
    '''
    algorithm = NSGAII(problem)# goes to the algorithm
    algorithm.run(500) #give value to run times (iterations)
    feasible_solutions = [s for s in algorithm.result if s.feasible]  ''' 
    '''
    for i in range(len(feasible_solutions)):
        for k in range(len(gv.bigres)):
            print(feasible_solutions[i].variables[k])
        print("*****************")
    '''    
    nondominanted_solutions=nondominated(algorithm.result)
    new = pd.DataFrame(nondominanted_solutions)  #rewriting the parameters back
    new.to_csv("nondominant.csv",sep=',',header=False,index=False,) 
    ned = pd.DataFrame(feasible_solutions)  #rewriting the parameters back
    ned.to_csv("feasible.csv",sep=',',header=False,index=False,) 

    return 
    
optimizer()    #starts calling the main program