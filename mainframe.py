"""
Created on Wed JAN 20 14:22:10 2020

@author: John JOSE
"""
#from test2 import input
from vector import permutation, indexfinder, reader, writer_of_vector
from platypus import *
from platypus import NSGAII, Problem, Real,nondominated,InjectedPopulation,Solution
from function import avg,ripple,rms,thd,moving_avg,peak
import circuit_solver as cs
import gv
import csv
import re
import pandas as pd
from plotter import plot, multiplot
import numpy as np
import externalvariable as ev
import globalfile as gf
gv.counter=0
def initalization():

    gv.c = 1  # global variable
    ev.uservariable()
    # optimizer  input intialisation
    variables = int(input("Enter no of elements to vary\nUser input: "))
    for res in range(0, variables):
        spec = []
        spec=input("Specify the element's parameters in the following format \n (element sheet no ,element row no ,max,min : )")
        spec=spec.split(",")
        spec.append(3)#column no:
        for i  in range(0,len(spec)):
            spec[i]=float(spec[i])
        gv.bigres.append(spec)  # combine to a large matrix global matrix in gv.py
    for r in range(0, len(gv.bigres)):
        print(gv.bigres[r])
    controlv=input("Do you need to vary a control variable with the algorithm? y/n \nUser input: ")
    if controlv == 'y':
        variables1 = int(input("Enter no of control variables to vary\nUser input: "))
        for i in range(variables1):
            spec = []
            spec.append(int(input("Enter the control variable index in python number format starting from 0\nUser input: ")))
            spec.append(-1) # dummy values to adjust the matrix and these values will be used to distigiung the elements and control variables
            spec.append(float(input('Enter maximum value of the control value\nUser input: ')))
            spec.append(float(input('Enter minimum value of the control value\nUser input: ')))
            gv.bigres.append(spec)
        variables=variables+variables1
    if gv.vector != 2:
        outpu = int(input("Enter no of output parameters to optimize\nUser input: "))
        for out in range(1, outpu + 1):
            outer = []
            rval = float(input("\n\nFunctions available:\n1.Average\n2.Ripple\n3.RMS\n4.THD\n5.Moving Average\n6.Peak\n7Optimizing an external variable or expression\nUser input: "))  # take mean set as an target value
            outer.append(rval)
            if rval==7:
                posoffile = int(input("Enter the  variable list no\nUser input: "))
                outer.append(posoffile)
                outer.append(9)#junk value to make it work
            else:
                posoffile = int(input("Enter the  output file no\nUser input: "))
                outer.append(posoffile-1)
                pos = int(input("Enter output meter no in output file\nUser input: "))
                outer.append(pos-1)
            ole=input("Enter the max and min limits of the output in the following format \n ( max,min)")
            ole =ole.split(",")#ole is a list of max and min values
            me=(float(ole[0])+float(ole[1]))/2
            outer.append(me)
            outer.append(2.5)#dummmy value to store future values
            gv.bigout.append(outer)  # update to a global matix
            for r in range(0, len(gv.bigout)):
                print(gv.bigout[r])
        gv.constraint=input("Do you want add constraint?\n press y/n\n")
        if gv.constraint == "y":
            con = int(input("Enter the no of constraints?\nUser input: "))
            for kup in range(con):
                kooper=[]                                                  #creation of a constraint matrix
                tat  = int(input("Enter variable list number\nUser input: "))         #variable list number
                tata = gv.externalvariable[tat-1]
                kooper.append(tata.value)
                kup2=int(input("Enter the constraint no:\n1.<=0\n2.>=0\nUser input: "))     #constraint type is specified
                kooper.append(kup2)
                gv.bigconst.append(kooper)
        print("\n\n The algorithms available for the user are:\n1.NSGAII\n2.NSGAIII\n3.CMAES\n4.GDE3\n5.IBEA\n6.MOEAD\n7.OMOPSO\n8.SMPSO\n9.SPEA2\n10.EpsMOEA\nPlease choose one of them by selecting the specified number :")
        gv.algoindex = int(input("User input:"))
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
    print("\nThe counter value is ", gv.counter)
    for m in range(0, len(gv.bigres)):
        if gv.bigres[m][1] == -1:
            controlvariableindex = gv.bigres[m][0]
            gf.controlvariable[controlvariableindex]=vars[m]
            print("\nThe  current value of  element" ,m,"is :",vars[m])
        else:
            flname = int(gv.bigres[m][0]) #the no in the params
            a = int(gv.bigres[m][1])  # write parameters to the circuit para meters
            b = int(gv.bigres[m][4])
            write(flname,a-1, b, vars[m])  # vars is the output from the prediction of genetic algorithm
            print("\nThe  current value of  element", m, "is :", vars[m])
    cs.main()
    ev.uservariable()
    #simulator is done
    gv.optotimer = 1
    gv.vectotimer = 1
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
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = moving_avg(lul,lol)
            gv.bigout[n][4] = x
            # print("this is moving average",x)
        elif gv.bigout[n][0] == 6:
            lol = gv.bigout[n][2]
            lul = gv.bigout[n][1]
            x = peak(lul,lol)
            gv.bigout[n][4] = x
            # print("this is peak",x)
        elif gv.bigout[n][0] == 7:
            lol = gv.bigout[n][1] # the variable location
            gv.bigout[n][4]=(gv.externalvariable[lol-1]).value  #gets the variables value
    if gv.constraint != 'y':
        lis = []
        for n in range(0, len(gv.bigout)):
            a = (gv.bigout[n][4] - gv.bigout[n][3]) ** 2
            if gv.bigout[n][3] >= 0:
                tru = gv.bigout[n][3]-a**0.5
                print("\n The value of  target ",n + 1," is ",tru," and the corresponding error value is ",a,"\n")
            else:
                tru = gv.bigout[n][3] + a** 0.5
                print(" The value of  target ",n + 1, " is " ,tru, " and the corresponding error value is ",a,"\n")
            lis.append(a)  # returns result out put to genetic algorithm
        return lis
    if gv.constraint == 'y':
        coco=[]
        for kio in range(len(gv.bigconst)):
            coco.append(gv.bigconst[kio][0])
        lis = []
        for n in range(0, len(gv.bigout)):
            a = (gv.bigout[n][4] - gv.bigout[n][3]) ** 2
            if gv.bigout[n][3] >= 0:
                tru = gv.bigout[n][3]-a**0.5
                print("\n The value of  target ",n + 1," is ",tru," and the corresponding error value is ",a,"\n")
            else:
                tru = gv.bigout[n][3] + a** 0.5
                print(" The value of  target ",n + 1, " is " ,tru, " and the corresponding error value is ",a,"\n")
            lis.append(a)  # returns result out put to genetic algorithm
        return lis,coco


#-------------------------------------------------------------------------------------------------------------------------------------------
def ga(variables, outpu):#genetic algorithm function
    if gv.vector==0:
        gv.algo=int(input("Enter the no: of iterations\nuser input: "))
        print(" \n*****  Optimization  procedures have started. *****\n")
    if gv.constraint == "n":
        problem = Problem(variables, outpu)
    if gv.constraint == "y":
        problem = Problem(variables, outpu,len(gv.bigconst))  # specify the no of objectives and inputs
    for i in range(0, len(gv.bigres)):
        problem.types[i:i + 1] = [Real(gv.bigres[i][3], gv.bigres[i][2])]  # loop to intialise the limkits
    for i in range(0, len(gv.bigconst)):
        for j in range(len(gv.bigconst[i])):
            if gv.bigconst[i][j] == 1:
                problem.constraints[i:i + 1] = "<=0"   #constraint assigning
            elif gv.bigconst[i][j] == 2:
                problem.constraints[i:i + 1] = ">=0"
    problem.function = evaluator  # call the simulator
    v_population_size = 10
    init_pop = [Solution(problem) for i in range(v_population_size)]
    pop_indiv = [[x.rand() for x in problem.types] for i in range(v_population_size)]

    for i in range(v_population_size):
        init_pop[i].variables = pop_indiv[i]

    if gv.algoindex == 1:
        algorithm = NSGAII(problem, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 2:
        algorithm = NSGAIII(problem,12, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 3:
        algorithm = CMAES(problem, epsilons =0.05, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 4:
        algorithm = GDE3(problem,  population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 5:
        algorithm = IBEA(problem, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 6:
        algorithm = MOEAD(problem,divisions_outer= 12, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 7:
        algorithm = OMOPSO(problem,epsilons= 0.05, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 8:
        algorithm = SMPSO(problem, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 9:
        algorithm = SPEA2(problem, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    elif gv.algoindex == 10:
        algorithm = EpsMOEA(problem,epsilons= 0.05, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    algorithm.run(gv.algo)
    feasible_solutions = [s for s in algorithm.result if s.feasible]
    nondominanted_solutions = nondominated(algorithm.result)
    f = open("feasible.txt", "a")
    f.write("\nThis is a set of feasible_solutions values\n")
    f.close()
    for ki in range(len(feasible_solutions)):
        f = open("feasible.txt", "a")
        f.write("\n This is solution  " + str(ki + 1) + "\n")
        f.close()
        for i in range(len(feasible_solutions[ki].variables)):
            f = open("feasible.txt", "a")
            f.write(  " The value of  element " + str(i+1)+" is " + str(feasible_solutions[ki].variables[i]) + "\n")
            f.close()
        for i in range(len(feasible_solutions[ki].objectives)):
            f = open("feasible.txt", "a")
            #f.write( "The  error  of target " +str(i+1) + " is  " + str(feasible_solutions[ki].objectives[i]) + "\n")
            if gv.bigout[i][3] >= 0:
                tru = gv.bigout[i][3]-feasible_solutions[ki].objectives[i]**0.5
                f.write(" The value of  target " + str(i + 1)  + " is " + str(tru) + " and the corresponding error value is " + str(feasible_solutions[ki].objectives[i]) + "\n")
            else:
                tru = gv.bigout[i][3] + feasible_solutions[ki].objectives[i] ** 0.5
                f.write(" The value of  target " + str(i + 1) + " is " + str(tru) + " and the corresponding error value is " + str(feasible_solutions[ki].objectives[i]) + "\n")
            f.close()
    f = open("nondominanted_solutions.txt", "a")
    f.write("\nThis is a set of nondominanted_solutions values\n")
    f.close()
    for ki in range(len(nondominanted_solutions)):
        f = open("nondominanted_solutions.txt", "a")
        f.write("\n This is solution  " + str(ki + 1) + "\n")
        f.close()
        for i in range(len(nondominanted_solutions[ki].variables)):
            f = open("nondominanted_solutions.txt", "a")
            f.write(" The value of  element " + str(i + 1) + " is " + str(nondominanted_solutions[ki].variables[i]) + "\n")
            f.close()
        for i in range(len(nondominanted_solutions[ki].objectives)):
            f = open("nondominanted_solutions.txt", "a")
            #f.write(str(i+1) + " th  objective error " + " value is " + str(nondominanted_solutions[ki].objectives[i]) + "\n")
            if gv.bigout[i][3] >= 0:
                tru = gv.bigout[i][3]-nondominanted_solutions[ki].objectives[i]**0.5
                f.write(" The value of  target " + str(i + 1)  + " is " + str(tru) + " and the corresponding error value is " + str(nondominanted_solutions[ki].objectives[i]) + "\n")
            else:
                tru = gv.bigout[i][3] + nondominanted_solutions[ki].objectives[i] ** 0.5
                f.write(" The value of  target " + str(i + 1) + " is " + str(tru) + " and the corresponding error value is " + str(nondominanted_solutions[ki].objectives[i]) + "\n")

            f.close()

    return

#-------------------------------------------------------------------------------------------------------------------------------------------
def starter():#user initialisation

    cs.main()
    a=input("Do you want to plot?\n y/n\nUserinput:")
    if a=='y':
        b=input("Plotting options available are press the no  eg 1 or 2:\n1.Single plot\n2.Multiplot\nUser input: ")
        if b=='2':
            multiplot()
        else:
            go='y'
            while(go=='y'):
                flname=gf.outputarray[int(input("Enter the output file no you want to plot?\nUser input: "))-1]
                meterno=int(input("Enter the Meter number\nUser input: "))
                title=input("Enter the title of the plot\nUser input: ")
                plot(flname,meterno,title)
                go=input("Do you want to plot again?\n y/n\n")
    appa = input("Do you want to compute any functions \npress y/n\nUserinput: ")
    if appa == 'y':
        while appa == 'y':
            rval = int(input("Functions available:\n1.Average\n2.Ripple\n3.RMS\n4.THD\n5.Moving Average\n6.Peak\n7.Optimizing an external variable or expression\nUser input: "))  # compute vallues
            if (rval == 1):
                num = (int(input("Enter file output number\nUser input: ")) - 1)
                rval1 = (int(input("Enter the meter number\nUser input: ")) - 1)
                print(avg(num,rval1))
            if (rval == 2):
                num = (int(input("Enter file output number\nUser input: ")) - 1)
                rval1 = (int(input("Enter the meter number\nUser input: "))-1)
                print(ripple(num,rval1))
            if (rval == 3):
                num = (int(input("Enter file output number\nUser input: ")) - 1)
                rval1 = (int(input("Enter the meter number\nUser input: "))-1)
                print(rms(num,rval1))
            if (rval == 4):
                num = (int(input("Enter file output number\nUser input: ")) - 1)
                rval1 = (int(input("Enter the meter number\nUser input: "))-1)
                print(thd(num,rval1))
            if (rval == 5):
                num = (int(input("Enter file output number\nUser input: ")) - 1)
                rval1 = (int(input("Enter the meter number\nUser input: "))-1)
                print(moving_avg(num,rval1))
            if (rval == 6):
                num = (int(input("Enter file output number\nUser input: ")) - 1)
                rval1 = (int(input("Enter the meter number\nUser input: "))-1)
                print(peak(num,rval1))
            if (rval == 7):
                posoffile = int(input("Enter the  variable list no\nUser input: "))
                ev.uservariable()
                print((gv.externalvariable[posoffile - 1]).value)
            appa = input("Do you want to compute any functions press y/n\n")

    opt=input("Do you want to optimize?\n y/n\n")
    if(opt=='y'):
        f = open("feasible.txt", "w")
        f.write(" The results are given below\n")
        f.close()
        f = open("nondominanted_solutions.txt", "w")
        f.write(" The results are given below\n")
        f.close()
        feat=int(input("Which of the following feature do you want?\n 1.Optimization \n 2.Topology change and Optimization\nUser input: "))
        if(feat==1):
            initalization()
        elif(feat==2):
            vctmain()
    return


def vctmain():
    gv.algo = int(input("Enter the no: of iterations in each vectorization instance?\nUser input: "))  # the no of iterations in each veactorization instance
    n = int(input("Enter the no of elements addresses to change\nUser input: ")) # eneter the no of elements in which vectorization is to be done
    gv.ele_chg = n
    for i in range(0, n):
        spec = input("Specify the element's parameters in the following format \n (element ckt file no ,element address,polarity address : )")
        spec = spec.split(",")  #take splitting of files
        spec[0]=int(spec[0])
        gv.bigvect.append(spec)
        #se = input("pleases specify if ")
        ''' this loop just took done the ckt file no details and elemanet addreses in coma format then turns no from string to 
        an integer so as to process it later on'''
    address=[]
    elements=[]
    for i in range(n):
        value1 = indexfinder(gv.bigvect[i][1])  #find indexes to search and spot parameters
        element = reader(gv.bigvect[i][0],value1)
        address.append(gv.bigvect[i][1])  #added upto address matrixes
        elements.append(element)
        #print(elements)
    superlist=permutation(elements) #creates a super list
    #print(superlist)
    gv.vector= 1
    initalization()
    chi ="n"
    #chi = input("do you want to keep same initialisation file for all run?\ny/n\n")
    print(" please note: after each combination in vectorisation it is mandatory to update the parameter details")
    if chi =='y':
        gv.inti_repeat = 1
    for i in range(0,len(superlist)):
        for j in range(0,len(address)):
            writer_of_vector(address[j], superlist[i][j],gv.bigvect[j][0])
            x = re.split("\_", superlist[i][j])  # split the file at '_'
            #print(x[0]) #debug
            if x[0]=="Capacitor":  #"check for polar elemnet"
                fileno=gv.bigvect[j][0]
                with open(gf.paramsarray[int(fileno) - 1], 'r') as f:
                    readprofile = csv.reader(f)  # read parameter file
                    urlize = list(readprofile)  # converting parameter file as a list
                index=100
                for k in range(len(urlize)):
                    if x[0]==urlize[k][0]:#find the capacitor elemnt
                        index=k
                        urlize[k][1]=urlize[k][1].replace(' ', '') #replace the extra character in the second element
                    if str(x[1]) == str(urlize[k][1]):
                        index1=k
                        if index == index1:   #find elemnt name

                            urlize[k][4] = "Positive polarity towards (cell) = "+str(gv.bigvect[j][2]) .upper()# assigning polarity  value to the list
                new = pd.DataFrame(urlize)  # rewriting the parameters back
                new.to_csv(gf.paramsarray[int(fileno) - 1], sep=',', header=False, index=False, )

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
        ga(len(gv.bigres), len(gv.bigout))
        if gv.inti_repeat == 0: # 0 must be the one but currently working on using same initialisation file
            gv.bigres.clear()
            #gv.bigout.clear()
            gv.vector = 2
            initalization()


    return


if __name__ == "__main__":
    starter()





