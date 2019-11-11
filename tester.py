import numpy as np

import gv

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
   