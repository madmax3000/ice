"""
Created on Wed JAN 20 14:22:10 2020

@author: John JOSE
"""
#from test2 import input
from vector import permutation, indexfinder, reader, writer_of_vector
from platypus import NSGAII, Problem, Real,nondominated,InjectedPopulation,Solution
from function import avg,ripple,rms,thd,efficiency,moving_avg,peak
import circuit_solver as cs
import gv
import csv
import pandas as pd
from plotter import plot, multiplot
import numpy as np
import externalvariable as ev
import globalfile as gf
gv.counter=0
def initalization():
    print(" \n!!!!  optimization algorithum is running   !!!!\n")
    gv.c = 1  # global variable
    # optimizer  input intialisation
    #gv.paramsfile=input("Enter circuit_params_file name\n")
    variables = int(input("enter no of elements to vary\n"))
    for res in range(0, variables):
        spec = []
        spec=input("Specify the element's parameters in the following format \n (element sheet no ,element row no ,max,min)")
        spec=spec.split(",")
        spec.append(3)#column no:
        for i  in range(0,len(spec)):
            spec[i]=float(spec[i])
        gv.bigres.append(spec)  # combine to a large matrix global matrix in gv.py
    for r in range(0, len(gv.bigres)):
        print(gv.bigres[r])
    #gv.outpu1 = input("Enter the output file in which the optimization targets are present \n ")
    outpu = int(input("enter no of output parameters to optimize"))
    for out in range(1, outpu + 1):
        outer = []
        rval = float(input("functions available:\n1 for avg\n2 for ripple\n3 for rms \n 4 for THD\n5 for efficency in percentage \n6 for moving average\n7 for peak\n8for optimizing an external variable or expression"))  # take mean set as an target value
        outer.append(rval)
        if rval==5:
            gv.esse.append(int(input("enter the meter no of output voltage:\n"))-1)#enter the output voltage meter no
            gv.esse.append(int(input("enter the meter no of output current:\n"))-1)  # enter the output current meter no
            gv.esse.append(int(input("enter the meter no of input voltage:\n"))-1)  # enter the input voltage meter no
            gv.esse.append(int(input("enter the meter no of input current:\n"))-1)  # enter the input current meter no
            outer.append(9) #junk value to make the matrix work as a charm
            outer.append(8)  # junk value to get the matrix right it is used to make squared error works for all
        if rval==8:
            posoffile = int(input("enter the  variable list no"))
            outer.append(posoffile)
            outer.append(9)#junk value to make it work
        else:
            posoffile = int(input("enter the  output file no"))
            outer.append(posoffile-1)
            pos = int(input("enter output meter no in output file "))
            outer.append(pos-1)
        ole=input("Enter the max and min limits of the output in the following format \n ( max,min)")
        ole =ole.split(",")#ole is a list of max and min values
        me=(float(ole[0])+float(ole[1]))/2
        outer.append(me)
        outer.append(2.5)#dummmy value to store future values
        gv.bigout.append(outer)  # update to a global matix
        for r in range(0, len(gv.bigout)):
            print(gv.bigout[r])
    if (gv.vector==0):
        ga(variables, outpu)  # call genetic algorithm
    return

#-----------------------------------------------------------------------------------------------------------------------------------
def write(flname,a, b, c):
    '''
    f = pd.read_csv(gv.paramsfile, header=False, index=False, )
    f.iloc[a, b] = c
    f.to_csv(gv.paramsfile, sep=',', header=False, index=False, )
    '''
    with open(gf.paramsarray[flname-1], 'r') as f:
        reader = csv.reader(f)  # read parameter file
        urlist = list(reader)  # converting parameter file as a list
    urlist[a][b] = c  # assigning parameter value to the list
    new = pd.DataFrame(urlist)  # rewriting the parameters back
    new.to_csv(gf.paramsarray[flname-1], sep=',', header=False, index=False, )
    return
#---------------------------------------------------------------------------------------------------------------------------------

def evaluator(vars):
    gv.counter = gv.counter + 1
    print("the counter value is ", gv.counter)
    for m in range(0, len(gv.bigres)):
        flname = int(gv.bigres[m][0]) #the no in the params
        a = int(gv.bigres[m][1])  # write parameters to the circuit para meters
        b = int(gv.bigres[m][4])
        write(flname,a-1, b, vars[m])  # vars is the output from the prediction of genetic algorithm
    cs.main()
    ev.uservariable()
    for n in range(0, len(gv.bigout)):
        if gv.bigout[n][0] == 1.0:  # read circuit output parameters
            lol = gv.bigout[n][2] #it has the file no of params file so it find the right file name
            lul = gv.bigout[n][1] #it has the meter number
            x = avg(lul,lol)
            gv.bigout[n][4] = x
            # print("this is avg value",x)
        elif gv.bigout[n][0] == 2:
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = ripple(lul,lol)
            gv.bigout[n][4] = x
            # print("this is ripple",x)
        elif gv.bigout[n][0] == 3:
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = rms(lul,lol)
            gv.bigout[n][4] = x
            # print("this is rms",x)
        elif gv.bigout[n][0] == 4:
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = thd(lul,lol)
            gv.bigout[n][4] = x
            # print("this is thd",x)
        elif gv.bigout[n][0] == 5:
            x = efficiency() # returns the current efficency
            gv.bigout[n][4] = x #places to an early dummy value
            # print("this is efficency",x)
        elif gv.bigout[n][0] == 6:
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = moving_avg(lul,lol)
            gv.bigout[n][4] = x
            # print("this is moving average",x)
        elif gv.bigout[n][0] == 7:
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = peak(lul,lol)
            gv.bigout[n][4] = x
            # print("this is peak",x)
        elif gv.bigout[n][0] == 8:
            lol = gv.bigout[n][1] # the variable location
            gv.bigout[n][4]=(gv.externalvariable[lol-1]).value  #gets the variables value
    lis = []
    for n in range(0, len(gv.bigout)):
        a = (gv.bigout[n][4] - gv.bigout[n][3]) ** 2
        lis.append(a)  # returns result out put to genetic algorithm

    return lis

#-------------------------------------------------------------------------------------------------------------------------------------------
def ga(variables, outpu):#genetic algorithm function
    if gv.vector==0:
        gv.algo=int(input("Enter the no: of iterations"))
    problem = Problem(variables, outpu)  # specify the no of objectives and inputs
    for i in range(0, len(gv.bigres)):
        problem.types[i:i + 1] = [Real(gv.bigres[i][3], gv.bigres[i][2])]  # loop to intialise the limkits

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
    f.write("\nthis is a set of feasible_solutions values\n")
    f.close()
    for i in range(len(feasible_solutions[0].variables)+1):
        f = open("feasible.txt", "a")
        f.write(str(i+1) + " th element" + " value is " + str(feasible_solutions[0].variables[i]) + "\n")
        f.close()
    for i in range(len(feasible_solutions[0].objectives)):
        f = open("feasible.txt", "a")
        f.write(str(i+1) + " th  objective error " + " value is " + str(feasible_solutions[0].objectives[i]) + "\n")
        f.close()
    f = open("nondominanted_solutions.txt", "a")
    f.write("\nthis is a set of nondominanted_solutions values\n")
    f.close()
    for i in range(len(nondominanted_solutions[0].variables)+1):
        f = open("nondominanted_solutions.txt", "a")
        f.write(str(i+1) + " th element" + " value is " + str(nondominanted_solutions[0].variables[i]) + "\n")
        f.close()
    for i in range(len(nondominanted_solutions[0].objectives)):
        f = open("nondominanted_solutions.txt", "a")
        f.write(str(i+1) + " th  objective error " + " value is " + str(nondominanted_solutions[0].objectives[i]) + "\n")
        f.close()

    return

#-------------------------------------------------------------------------------------------------------------------------------------------
def starter():#user initialisation

   # cs.main()
    a=input("Do you want to plot?\n y or n")
    if a=='y':
        b=input("plotting options available are:\n1.single plot\n2.multiplot")
        if b=='2':
            multiplot()
        else:
            go='y'
            while(go=='y'):
                flname=input("Enter the output file which you want to plot?\n")
                meterno=int(input("Enter the Meter number\n"))
                title=input("Enter the title of the plot\n")
                plot(flname,meterno,title)
                go=input("Do you want to plot again?\n y or n")

    opt=input("Do you want to optimize?\n y or n")
    if(opt=='y'):
        feat=int(input("Which of the following feature do you want?\n 1.Optimization \n 2.Topology change and Optimization"))
        if(feat==1):
            initalization()
        elif(feat==2):
            vctmain()
    return


def vctmain():
    n = int(input("enter the no of elements to change")) # eneter the no of elements in which vectorization is to be done
    gv.algo = int(input("Enter the no: of iterations in each vectorization instance?")) # the no of iterations in each veactorization instance
    for i in range(0, n):
        spec = input("Specify the element's parameters in the following format \n (element ckt file no ,element address)")
        spec = spec.split(",")
        spec[0]=int(spec[0])
        gv.bigvect.append(spec)
        ''' this loop just took done the ckt file no details and elemanet addreses in coma format then turns no from string to 
        an integer so as to process it later on'''
    address=[]
    elements=[]
    for i in range(n):
        value1 = indexfinder(gv.bigvect[i][1])
        element = reader(gv.bigvect[i][0],value1)
        address.append(gv.bigvect[i][1])
        elements.append(element)
        print(elements)
    superlist=permutation(elements)
    print(superlist)


    ''' the above session just read the elemnt names from the respective lists 
    and then it would create a permutation of elemants so that all combinations could be tried out.'''


    '''
    gv.cktfile = input("enter the filename in which vectorization is to be done:\n")
    

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
    '''
    gv.vector= 1
    initalization()
    chi = input("do you want to keep same initialisation file for all run?\ny/n\n")
    if chi =='y':
        gv.inti_repeat = 1
    for i in range(0,len(superlist)):
        for j in range(0,len(address)):
            writer_of_vector(address[j], superlist[i][j],gv.bigvect[j][0])
            f = open("feasible.txt", "a")
            f.write("\n")
            f.write(superlist[i][j])    #writing before each file creation to see list positions
            f.write("   address: ")
            f.write(address[j])
            f.close()
            f = open("nondominanted_solutions.txt", "a")
            f.write("\n")
            f.write(superlist[i][j])
            f.write("   address: ") #nondominated solutions have option for writing properly
            f.write(address[j])
            f.close()
        if gv.inti_repeat == 0:
            initalization()
        ga(len(gv.bigres),len(gv.bigout))
    return


if __name__ == "__main__":
    starter()





