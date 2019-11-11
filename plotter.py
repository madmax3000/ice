# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 05:55:17 2019

@author: JOHN
"""
import numpy as np
from matplotlib import pyplot as plt
def plot():
    data=np.loadtxt('ckt_output.dat')
    X=data[:,0]
    Y=data[:,1]
    Z=data[:,2]
    plt.plot(X,Y,':ro')
    plt.show()
    plt.plot(X,Z,':bo')
    plt.show()