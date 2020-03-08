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
import re
import pandas as pd
from plotter import plot, multiplot
import numpy as np
import externalvariable as ev
import globalfile as gf
gv.counter=0
def initalization():
    print(" \n!!!!  optimization algorithum procedures have started.   !!!!\n")
    gv.c = 1  # global variable
    ev.uservariable()
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
        rval = float(input("functions available:\n1 for avg\n2 for ripple\n3 for rms\n4 for THD\n5 for moving average\n6 for peak\n7for optimizing an external variable or expression"))  # take mean set as an target value
        outer.append(rval)
        if rval==100: # will be deleted later
            gv.esse.append(int(input("enter the meter no of output voltage:\n"))-1)#enter the output voltage meter no
            gv.esse.append(int(input("enter the meter no of output current:\n"))-1)  # enter the output current meter no
            gv.esse.append(int(input("enter the meter no of input voltage:\n"))-1)  # enter the input voltage meter no
            gv.esse.append(int(input("enter the meter no of input current:\n"))-1)  # enter the input current meter no
            outer.append(9) #junk value to make the matrix work as a charm
            outer.append(8)  # junk value to get the matrix right it is used to make squared error works for all
        if rval==7:
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
    gv.constraint=input("do you want add constraint?\n press y or n\n")
    if gv.constraint == "y":
        con = int(input("enter the no of constraints?"))
        for kup in range(con):
            kooper=[]                                                  #creation of a constraint matrix
            tat  = int(input("enter variable list number : "))         #variable list number
            tata = gv.externalvariable[tat]
            kooper.append(tata.value)
            kup2=int(input("enter the constraint no:\n1.<=0\n2.>=0"))     #constraint type is specified
            kooper.append(kup2)
            gv.bigconst.append(kooper)
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
    print("simulation running started")
    cs.main()
    ev.uservariable()
    print("simulation running stopped")
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
        elif gv.bigout[n][0] == 100:   #will delete later
            x = efficiency() # returns the curr ent efficency
            gv.bigout[n][4] = x #places to an early dummy value
            # print("this is efficency",x)
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
            lis.append(a)  # returns result out put to genetic algorithm
        return lis
    if gv.constraint == 'y':
        coco=[]
        for kio in range(len(gv.bigconst)):
            coco.append(gv.bigconst[kio][0])
        lis = []
        for n in range(0, len(gv.bigout)):
            a = (gv.bigout[n][4] - gv.bigout[n][3]) ** 2
            lis.append(a)  # returns result out put to genetic algorithm
        return lis,coco


#-------------------------------------------------------------------------------------------------------------------------------------------
def ga(variables, outpu):#genetic algorithm function
    if gv.vector==0:
        gv.algo=int(input("Enter the no: of iterations"))
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

    algorithm = NSGAII(problem, population_size=v_population_size, generator=InjectedPopulation(init_pop))
    algorithm.run(gv.algo)
    feasible_solutions = [s for s in algorithm.result if s.feasible]
    nondominanted_solutions = nondominated(algorithm.result)
    f = open("feasible.txt", "a")
    f.write("\nthis is a set of feasible_solutions values\n")
    f.close()
    for ki in range(len(feasible_solutions)):
        f = open("feasible.txt", "a")
        f.write("\n this is solution  " + str(ki + 1) + "\n")
        f.close()
        for i in range(len(feasible_solutions[ki].variables)):
            f = open("feasible.txt", "a")
            f.write(str(i+1) + " th element" + " value is " + str(feasible_solutions[ki].variables[i]) + "\n")
            f.close()
        for i in range(len(feasible_solutions[ki].objectives)):
            f = open("feasible.txt", "a")
            f.write(str(i+1) + " th  objective error " + " value is " + str(feasible_solutions[ki].objectives[i]) + "\n")
            f.close()
    f = open("nondominanted_solutions.txt", "a")
    f.write("\nthis is a set of nondominanted_solutions values\n")
    f.close()
    for ki in range(len(nondominanted_solutions)):
        f = open("nondominanted_solutions.txt", "a")
        f.write("\n this is solution  " + str(ki + 1) + "\n")
        f.close()
        for i in range(len(nondominanted_solutions[ki].variables)):

            f = open("nondominanted_solutions.txt", "a")
            f.write(str(i+1) + " th element" + " value is " + str(nondominanted_solutions[ki].variables[i]) + "\n")
            f.close()
        for i in range(len(nondominanted_solutions[ki].objectives)):
            f = open("nondominanted_solutions.txt", "a")
            f.write(str(i+1) + " th  objective error " + " value is " + str(nondominanted_solutions[ki].objectives[i]) + "\n")
            f.close()

    return

#-------------------------------------------------------------------------------------------------------------------------------------------
def starter():#user initialisation

    cs.main()
    a=input("Do you want to plot?\n y or n")
    if a=='y':
        b=input("plotting options available are:\n1.single plot\n2.multiplot")
        if b=='2':
            multiplot()
        else:
            go='y'
            while(go=='y'):
                flname=gf.outputarray[int(input("Enter the output file no you want to plot?\n"))-1]
                meterno=int(input("Enter the Meter number\n"))
                title=input("Enter the title of the plot\n")
                plot(flname,meterno,title)
                go=input("Do you want to plot again?\n y or n")
    appa = input("do you want to compute any values from the data like avg,rms,etc? press y or n")
    if appa == 'y':
        while appa == 'y':
            rval = int(input("functions available:\n1 for avg\n2 for ripple\n3 for rms \n 4 for THD\n5 for moving average\n6 for peak\n7for optimizing an external variable or expression"))  # compute vallues
            if (rval == 1):
                num = (int(input("enter file output number")) - 1)
                print(avg(num,rval))
            if (rval == 2):
                num = (int(input("enter file output number")) - 1)
                print(ripple(num,rval))
            if (rval == 3):
                num = (int(input("enter file output number")) - 1)
                print(rms(num,rval))
            if (rval == 4):
                num = (int(input("enter file output number")) - 1)
                print(thd(num,rval))
            if (rval == 5):
                num = (int(input("enter file output number")) - 1)
                print(moving_avg(num,rval))
            if (rval == 6):
                num = (int(input("enter file output number")) - 1)
                print(peak(num,rval))
            if (rval == 7):
                posoffile = int(input("enter the  variable list no"))
                ev.uservariable()
                print((gv.externalvariable[posoffile - 1]).value)
            appa = input("do you want to compute any values from the data like avg,rms,etc again? press y or n")

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
    gv.ele_chg = n
    gv.algo = int(input("Enter the no: of iterations in each vectorization instance?")) # the no of iterations in each veactorization instance
    for i in range(0, n):
        spec = input("Specify the element's parameters in the following format \n (element ckt file no ,element address,polarity address)")
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
        print(elements)
    superlist=permutation(elements) #creates a super list
    print(superlist)
    gv.vector= 1
    initalization()
    chi = input("do you want to keep same initialisation file for all run?\ny/n\n")
    if chi =='y':
        gv.inti_repeat = 1
    for i in range(0,len(superlist)):
        for j in range(0,len(address)):
            writer_of_vector(address[j], superlist[i][j],gv.bigvect[j][0])
            x = re.split("\_", superlist[i][j])  # split the file at '_'
            print(x[0]) #debug
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
                            urlize[k][4] = "Positive polarity towards (cell) = "+str(gv.bigvect[j][2]) # assigning polarity  value to the list
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
        if gv.inti_repeat == 0:
            initalization()
        ga(len(gv.bigres),len(gv.bigout))
    return


if __name__ == "__main__":
    starter()





