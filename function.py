
"""
Created on Wed Nov 20 14:22:10 2019

@author: JENSON JOSE
"""
import globalfile as gf
from scipy.fftpack import fft
from scipy.signal import savgol_filter as sv
import numpy as np
import pandas as pd
import gv
#import statistics
def data_extractor(outputarrayno,meterno):
    data = np.loadtxt(gf.outputarray[outputarrayno]) #load data
    x = data[:, meterno]  # read data file
    y = signalselector(x)   #signal selector is directly called
    return y
def signalselector(a):
    f = pd.read_csv("circuit_inputs.csv", header=None, index_col=False)
    ele = f.iloc[3,2]
    t2=float(ele) #t2-step size
    t1=1/60 #default time period
    #n1=len(a)#n1-total number of samples
    n2=t1/t2 #n2-number of samples in one time period t1
    gv.n3=int(n2)
    if len(a)<gv.n3:
        gv.n3=len(a)
    gv.l=[]
    for i in range(0,gv.n3):
        gv.l.append(a[i])
    #print (gv.l)
    return gv.l
    
def ripple(c,a):
    m=data_extractor(c,a)
    c=max(m)
    b=min(m)
    ripplev=c-b
    #print(ripplev)
    return ripplev
def avg(c,a):
    l=data_extractor(c,a)
    s=0
    for x in range(0,len(l)):
        s+=l[x]
    av=s/len(l)#average value
    #print(av,"this is the avg")
    return av

def rms(c,d):
    l=data_extractor(c,d)
    ms = 0
    for i in range(0,len(l)):
        ms = ms + l[i]*l[i]
    ms = ms / len(l)
    rms = np.sqrt(ms)
    #print(rms)
    return rms

def thd(c,n):
    t = data_extractor(c,n)
    abs_yf = np.abs(fft(t))
    abs_data = abs_yf
    sq_sum = 0.0
    for r in range(len(abs_data)):
       sq_sum = sq_sum + (abs_data[r])**2
    sq_harmonics = sq_sum-(max(abs_data))**2.0
    thd = 100*sq_harmonics**0.5/max(abs_data)
    return thd

def moving_avg(c,k):
    a=data_extractor(c,k)
    n=sv(a,5,2)
    s = 0
    for x in range(0, len(n)):
        s += n[x]
    av = s / len(n)  # average value
    return av #moving average implemented
def peak(c,m):
    a=data_extractor(c,m)
    c = max(a) #peak implemented
    return c