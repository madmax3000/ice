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
        x = float((input("Enter T-min")))
        y = float((input("Enter T-max")))
        data = np.loadtxt(flname)
        result = data[:, 0]
        #print(result)
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
        a = input("Do you want to specify the time period again.....y/n ")
def multiplot():
    #ckt_output2.dat

    n=int(input("How many plots do you want\n maximum 5 plots are only possible"))
    fl=input("enter the filename")
    mr=[]
    for i in range(n):
        mn=int(input("Enter meter numbers"))
        mr.append(mn)
    data = np.loadtxt(fl)
    X=data[:,0]
    if(n==2):
        Y1=data[:,mr[0]]
        Y2=data[:,mr[1]]
        plt.plot(X,Y1,label=mr[0])
        plt.plot(X, Y2,label=mr[1])
        plt.show()
    if (n == 3):
        Y1 = data[:, mr[0]]
        Y2 = data[:, mr[1]]
        Y3 = data[:, mr[2]]
        plt.plot(X, Y1,label=mr[0])
        plt.plot(X, Y2,label=mr[1])
        plt.plot(X, Y3,label=mr[2])
        plt.show()
    if (n == 4):
        Y1 = data[:, mr[0]]
        Y2 = data[:, mr[1]]
        Y3 = data[:, mr[2]]
        Y4 = data[:, mr[3]]
        plt.plot(X, Y1,label=mr[0])
        plt.plot(X, Y2,label=mr[1])
        plt.plot(X, Y3,label=mr[2])
        plt.plot(X, Y4, label=mr[3])
        plt.show()
    if (n == 5):
        Y1 = data[:, mr[0]]
        Y2 = data[:, mr[1]]
        Y3 = data[:, mr[2]]
        Y4 = data[:, mr[3]]
        Y5 = data[:, mr[4]]
        plt.plot(X, Y1,label=mr[0])
        plt.plot(X, Y2,label=mr[1])
        plt.plot(X, Y3,label=mr[2])
        plt.plot(X, Y4, label=mr[3])
        plt.plot(X, Y5, label=mr[4])
        plt.show()





