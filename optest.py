# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:18:45 2020

@author: JENSON JOSE
"""
from platypus import NSGAII, Problem, Real,nondominated
import pandas as pd
def belegundu(vars):
    x = vars[0]
    y = vars[1]
    m=(x+y-3)**2
    n=(2*x+2*y-6)**2
    return [m,n]

problem = Problem(2, 2)
problem.types[:] = [Real(0, 5), Real(0, 3)]
#problem.constraints[:] = "<=0"
problem.function = belegundu

algorithm = NSGAII(problem)
algorithm.run(100)
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
for i in range(len(feasible_solutions[0].objectives)):
    f = open("feasible_test.txt", "a")
    #f.write(str(i)+" th element" + " value is "+str(feasible_solutions[0].variables[i])+"\n")
    f.write(str(i) + " th  objective error " + " value is " + str(feasible_solutions[0].objectives[i]) + "\n")
    f.close()