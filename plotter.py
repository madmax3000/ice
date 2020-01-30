# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 05:55:17 2019

@author: JOHN
"""
import numpy as np
from matplotlib import pyplot as plt
def plot():
    data=np.loadtxt('ckt_output2.dat')
    x=1
    y=4500
    X=data[x:y,0]
    N=data[x:y,0]
    Y=data[x:y,2]
    Z=data[x:y,3]
    plt.plot(X,Y,'r',label='Inductor Current')
    plt.grid(True, color='k')
    plt.legend()
    plt.show()
    plt.plot(N,Z,'b',label='Output Voltage')
    plt.legend()
    plt.grid(True, color='k')
    plt.show()

