from test2 import input
from vector import permutation, indexfinder, reader, writer_of_vector
from platypus import NSGAII, Problem, Real,nondominated,InjectedPopulation,Solution
from function import avg,ripple,rms,signalselector,thd
import circuit_solver as cs
import gv
import csv
import pandas as pd
from plotter import plot
import numpy as np
gv.counter=0
def initalization():
    print(" \n!!!!  optimization algorithum is running   !!!!\n")
    gv.c = 1  # global variable
    # optimizer  input intialisation
    gv.paramsfile=input("Enter circuit_params_file name\n")
    variables = int(input("enter no of elements to vary\n"))
    for res in range(0, variables):
        spec = []
        spec=input("Specify the element's parameters in the following format \n (max,min,row)")
        spec=spec.split(",")
        spec.append(3)#column no:
        for i  in range(0,len(spec)):
            spec[i]=float(spec[i])
        gv.bigres.append(spec)  # combine to a large matrix global matrix in gv.py
    for r in range(0, len(gv.bigres)):
        print(gv.bigres[r])
    gv.outpu1 = input("Enter the output file in which the optimization targets are present \n ")
    outpu = int(input("enter no of output parameters to optimize"))
    for out in range(1, outpu + 1):
        outer = []
        pos = int(input("enter output meter no in output file "))
        outer.append(pos)
        rval = float(input("1 for avg\n2 for ripple\n3 for rms \n 4 for THD "))  # take mean set as an target value
        outer.append(rval)
        ole=input("Enter the max and min limits of the output in the following format \n ( max,min)")
        ole =ole.split(",")#ole is a list of max and min values
        me=(float(ole[0])+float(ole[1]))/2
        outer.append(me)
        outer.append(2.5)#
        gv.bigout.append(outer)  # update to a global matix
        for r in range(0, len(gv.bigout)):
            print(gv.bigout[r])
    if (gv.vector==0):
        ga(variables, outpu)  # call genetic algorithm
    return

#---------------------------------------------------------------------------------------------------------
def write(a, b, c):
    '''
    f = pd.read_csv(gv.paramsfile, header=False, index=False, )
    f.iloc[a, b] = c
    f.to_csv(gv.paramsfile, sep=',', header=False, index=False, )
    '''
    with open(gv.paramsfile, 'r') as f:
        reader = csv.reader(f)  # read parameter file
        urlist = list(reader)  # converting parameter file as a list
    urlist[a][b] = c  # assigning parameter value to the list
    new = pd.DataFrame(urlist)  # rewriting the parameters back
    new.to_csv(gv.paramsfile, sep=',', header=False, index=False, )

#-----------------------------------------------------------------------------------------------------------
def readus_avg(out):
    data = np.loadtxt(gv.outpu1)
    x = data[:, out]  # read data file
    y = signalselector(x)
    m = avg(y)
    return m
#----------------------------------------------------------------------------------------------------------

def readus_ripple(out):
    data = np.loadtxt(gv.outpu1)
    x = data[:, out]  # read data file
    y = signalselector(x)
    n = ripple(y)
    return n
#-------------------------------------------------------------------------------------------------------------

def readus_rms(out):
    data = np.loadtxt(gv.outpu1)
    x = data[:, out]  # read data file
    y = signalselector(x)
    p = rms(y)
    return p

#------------------------------------------------------------------------------------------------------------------
def readus_thd(out):
    data = np.loadtxt(gv.outpu1)
    x = data[:, out]  # read data file
    y = signalselector(x)
    th = thd(y)
    return th
#----------------------------------------------------------------------------------
def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1



#--------------------------------------------------------------------------------------------------------
def evaluator(vars):
    gv.counter = gv.counter + 1
    print("the counter value is ", gv.counter)
    for m in range(0, len(gv.bigres)):
        a = int(gv.bigres[m][2])  # write parameters to the circuit para meters
        b = int(gv.bigres[m][3])
        write(a, b, vars[m])  # vars is the output from the prediction of genetic algorithm
    cs.main()
    for n in range(0, len(gv.bigout)):
        if gv.bigout[n][3] == 1.0:  # read circuit output parameters
            lol = gv.bigout[n][0]
            x = readus_avg(lol - 1)
            gv.bigout[n][3] = x
            # print("this is avg value",x)
        else:
            lol = gv.bigout[n][0]
            x = readus_ripple(lol - 1)
            gv.bigout[n][3] = x
            # print("this is ripple",x)

    lis = []
    for n in range(0, len(gv.bigout)):
        a = (gv.bigout[n][2] - gv.bigout[n][3]) ** 2
        lis.append(a)  # returns result out put to genetic algorithm

    return lis

#-----------------------------------------------------------------------------------------------------------------
def ga(variables, outpu):#genetic algorithm function
    if gv.vector==0:
        gv.algo=int(input("Enter the no: of iterations"))
    problem = Problem(variables, outpu)  # specify the no of objectives and inputs
    for i in range(0, len(gv.bigres)):
        problem.types[i:i + 1] = [Real(gv.bigres[i][1], gv.bigres[i][0])]  # loop to intialise the limkits

    problem.function = evaluator  # call the simulator
    v_population_size = 10
    init_pop = [Solution(problem) for i in range(v_population_size)]
    pop_indiv = [[x.rand() for x in problem.types] for i in range(v_population_size)]

    for i in range(v_population_size):
        init_pop[i].variables = pop_indiv[i]

    algorithm = NSGAII(problem, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    algorithm.run(gv.algo)
    feasible_solutions = [s for s in algorithm.result if s.feasible]
    nondominanted_solutions = nondominated(algorithm.result)
    f = open("feasible.txt", "a")
    f.write("\nthis is a set of values\n")
    f.close()
    f = open("nondominanted_solutions.txt", "a")
    f.write("\nthis is a set of values\n")
    f.close()
    for st in range(len(feasible_solutions)):
        f = open("feasible.txt", "a")
        f.write(listToString(feasible_solutions[st].__str__()))
        f.write("\n")
        f.close()
    for tui in range(len(nondominanted_solutions)):
        f = open("nondominanted_solutions.txt", "a")
        f.write(listToString(nondominanted_solutions[tui].__str__()))
        f.write("\n")
        f.close()

    return

#-----------------------------------------------------------------------------------------------------------------------
def starter():#user initialisation
    cs.main()
    a=input("Do you want to plot?\n y or n")
    while(a=='y'):
        flname=input("Enter the output file which you want to plot?\n")
        meterno=int(input("Enter the Meter number\n"))
        title=input("Enter the title of the plot\n")
        plot(flname,meterno,title)
        a=input("Do you want to plot again?\n y or n")

    opt=input("Do you want to optimize?\n y or n")
    if(opt=='y'):
        feat=int(input("Which of the following feature do you want?\n 1.Optimization \n 2.Topology change and Optimization"))
        if(feat==1):
            initalization()
        elif(feat==2):
            vctmain()
    return


def vctmain():
    gv.cktfile = input("enter the filename in which vectorization is to be done:\n")
    gv.algo = int(input("Enter the no: of iterations in each vectorization instance?"))
    n = int(input("enter the no of elements to change"))
    addr = []
    elm = []
    superlist = []
    for i in range(0, n):
        y = input("enter the positions")
        addr.append(y)
        print(addr)
        m = indexfinder(addr[i])
        print(m)
        elm.append((reader(m)))
    superlist = permutation(elm)
    print(elm)
    print(superlist)
    gv.vector= 1
    initalization()
    chi = input("do you want to keep same initialisation file for all run?\ny/n\n")
    if chi =='y':
        gv.inti_repeat = 1
    for i in range(0,len(superlist)):
        for j in range(0,len(addr)):
            writer_of_vector(addr[j], superlist[i][j])
        if gv.inti_repeat == 0:
            initalization()
        ga(len(gv.bigres),len(gv.bigout))
    return


starter()




