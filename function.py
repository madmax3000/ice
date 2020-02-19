
"""
Created on Wed Nov 20 14:22:10 2019

@author: JENSON JOSE
"""
import gv
from scipy.fftpack import fft
from scipy.signal import savgol_filter as sv
import numpy as np
import pandas as pd
#import statistics
def data_extractor(out):
    data = np.loadtxt(gv.outpu1)
    x = data[:, out]  # read data file
    y = signalselector(x)
    return y
def signalselector(a):
    f = pd.read_csv("circuit_inputs.csv", header=None, index_col=False)
    ele = f.iloc[2,2]
    t2=float(ele) #t2-step size
    t1=1/60 #default time period
    #n1=len(a)#n1-total number of samples
    n2=t1/t2 #n2-number of samples in one time period t1
    gv.n3=int(n2)    
    
    for i in range(0,gv.n3):
        gv.l.append(a[i])
    #print (gv.l)
    return gv.l
    
def ripple(a):
    c=max(a)
    b=min(a)
    ripplev=c-b
    #print(ripplev)
    return ripplev
def avg(a):
    s=0
    for x in range(0,len(gv.l)):
        s+=gv.l[x]
    av=s/len(gv.l)#average value
    #print(av,"this is the avg")
    return av

def rms(d):
    ms = 0
    for i in range(0,gv.n3):
        ms = ms + gv.l[i]*gv.l[i]
    ms = ms / gv.n3
    rms = np.sqrt(ms)
    #print(rms)
    return rms

def thd(t):
    abs_yf=np.abs(fft(t))
    abs_data=abs_yf
    sq_sum=0.0
    for r in range(len(abs_data)):
       sq_sum=sq_sum+(abs_data[r])**2
    sq_harmonics=sq_sum-(max(abs_data))**2.0
    thd=100*sq_harmonics**0.5/max(abs_data)
    return thd
def efficiency():
    p1 = avg(data_extractor(gv.esse[0]))
    p2 = avg(data_extractor(gv.esse[1]))
    p3 = avg(data_extractor(gv.esse[2]))
    p4 = avg(data_extractor(gv.esse[3]))
    n=((p1*p2)/(p3*p4))
    return n*100
def moving_avg(a):
    n=sv(a,5,2)
    fs=len(n)
    return n[fs-1] #moving average implemented
def peak(a):
    c = max(a) #peak implemented
    return c