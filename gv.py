# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:36:30 2019

@author: JOHN
"""
c = 0# to stop seeing repeated steps
bigres=[]#the big matrix of parameters which can be changed
bigout=[]#the big matrix of output targets to be achieved
counter=0#debugging
l=[]#list which stores the samples produced during timeperiod t1
n3=0#for signal selector
algo=200#no of default iterations
outpu1="ckt_output.dat"#default value of output file name
paramsfile="ckt_params.csv" #default value of ckt params file
cktfile="ckt.csv" #default value of ckt
inti_repeat=0 #variable to stop repeated initialisation
vector=0 #variable to see if vectorization has taken place