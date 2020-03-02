# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:36:30 2019

@author: JOHN
"""
c = 0# to stop seeing repeated steps
bigres=[]#the big matrix of parameters which can be changed
bigout=[]#the big matrix of output targets to be achieved
bigvect=[]
counter=0#debugging
l=[]#list which stores the samples produced during timeperiod t1
n3=0#for signal selector
algo=10#no of default iterations
outpu1="ckt_output2.dat"#default value of output file name
paramsfile="ckt_params.csv" #default value of ckt params file
cktfile="ckt.csv" #default value of ckt
inti_repeat=0 #variable to stop repeated initialisation
vector=0 #variable to see if vectorization has taken place
esse=[] #list for efficency calculations
externalvariable=[]# used for storing external variables
time=0.0
optotimer=0
vectotimer=0
timetotal=0.0
ele_chg=2
#used for testing purpose
z=0#test2
k=0#test1,test2