# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 05:55:17 2019

@author: JOHN
"""

import numpy as np
from matplotlib import pyplot as plt

def plot(flname,meterno,ttl):
    data=np.loadtxt(flname)
    X=data[:,0]
    Y=data[:,meterno-1]
    plt.plot(X,Y,'r')
    plt.title(ttl)
    plt.show()
    a=input("do you want plot a specific range of values?\npress y or n\n")
    while(a=='y'):
        a = input("Do you want to specify the time period.....y/n ")
        x = float((input("Enter T-min")))
        y = float((input("Enter T-max")))
        data = np.loadtxt(flname)
        result = data[:, 0]
        print(result)
        t1 = 0
        t2 = 0
        c = 0
        for i in range(0, len(result)):
            if (result[i] >= x and c == 0):
                t1 = i
                c = 1
            if (result[i] <= y):
                t2 = i + 1
        X = data[t1:t2, 0]
        Y = data[t1:t2, meterno-1]
        plt.plot(X, Y, 'r')
        plt.title(ttl)
        plt.show()
#plot("ckt_output2.dat",4,"output_voltage")









