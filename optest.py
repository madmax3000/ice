# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:18:45 2020

@author: JENSON JOSE
"""
apa ="n"
from platypus import NSGAII, Problem, Real,nondominated
def belegundu(vars):
    x = vars[0]
    y = vars[1]
    m=(x+y-3)**2
    n=(2*x+2*y-6)**2
    k=-1+x
    l=1+y
    if apa =='y':
        return [m,n],[k,l]
    if apa =='n':
        return [m,n]
#a=none
apa=input("do you want constraints")
if apa == 'n':
    problem = Problem(2, 2)
if apa == 'y':
    problem = Problem(2, 2, 2)

problem.types[:] = [Real(0, 5), Real(0, 3)]
if apa =='y':
    problem.constraints[0:1] = "<=0"
    problem.constraints[1:2] = ">=0"
problem.function = belegundu

algorithm = NSGAII(problem)
algorithm.run(1000)
#print(algorithm.result)
feasible_solutions = [s for s in algorithm.result if s.feasible]
#print(feasible_solutions[0].variables[0])
#print("\n",feasible_solutions[0].variables[1])
#print(feasible_solutions[0].objectives[0])
nondominanted_solutions=nondominated(algorithm.result)
for i in range(len(feasible_solutions[0].variables)):
    f = open("feasible_test.txt", "a")
    f.write(str(i)+" th element" + " value is "+str(feasible_solutions[0].variables[i])+"\n")
    #f.write(str(i) + " th  objective error " + " value is " + str(feasible_solutions[0].objectives[i]) + "\n")
    f.close()
