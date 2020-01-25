def buck_control_func(interface_inputs, interface_outputs, interface_static, interface_time, interface_variablestore,                                 interface_events, circuit_components, pos, t_clock, sys_t_events):
	carr_signal=interface_static[pos]['carr_signal']
	t1=interface_time[pos]['t1']
	VarStor1=interface_variablestore['VarStor1'][0]
	VarStor2=interface_variablestore['VarStor2'][0]
	S1_gate=interface_outputs[pos]['1G0'][1][2]
	# -*- coding: utf-8 -*-
	"""
	Created on Mon Jan 20 13:07:59 2020
	
	@author: Goutham
	"""
	
	'''
	sw_freq=20000
	if t_clock>=t1:
	    
	    if S1_gate==1:
	            S1_gate = 0.0
	    else:
	        S1_gate = 1.0
	    t1=t1+(1/sw_freq)
	VarStor1=t1
	VarStor2=S1_gate
	'''
	sw_freq=20000
	dt=1.0e-6
	if t_clock>=t1:
	    carr_signal+=(1/(1/sw_freq))*dt
	    if carr_signal>1.0:
	        carr_signal=0.0
	    mod_signal=0.5
	    if mod_signal>carr_signal:
	        S1_gate=1.0
	    else:
	        S1_gate=0.0
	    t1+=dt
	VarStor1=carr_signal
	VarStor2=S1_gate

	interface_events[pos] = 0

	if not interface_outputs[pos]['1G0'][1][2]==S1_gate:
		interface_events[pos] = 1

	circuit_components['1G0'].control_values[0]=S1_gate
	interface_outputs[pos]['1G0'][1][2]=S1_gate
	interface_static[pos]['carr_signal']=carr_signal
	interface_time[pos]['t1']=t1
	sys_t_events.append(t1)
	interface_variablestore['VarStor1'][0]=VarStor1
	interface_variablestore['VarStor2'][0]=VarStor2
	return

