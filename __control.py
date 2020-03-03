import math

import math

def mag_transf_func(interface_inputs, interface_outputs, interface_static, interface_time, interface_variablestore,                                 interface_events, circuit_components, pos, t_clock, sys_t_events):
	v1meas=circuit_components['9F0'].op_value
	v2meas=circuit_components['9AE0'].op_value
	iprim=circuit_components['1O0'].op_value
	flux=interface_static[pos]['flux']
	curr_vector=interface_static[pos]['curr_vector']
	t1=interface_time[pos]['t1']
	T1_flux=interface_variablestore['T1_flux'][0]
	VarStor1=interface_variablestore['VarStor1'][0]
	VT1wdg1=interface_outputs[pos]['8S0'][1][2]
	VT1wdg2=interface_outputs[pos]['8U0'][1][2]
	RT1wdg1=interface_outputs[pos]['1K0'][1][2]
	RT1wdg2=interface_outputs[pos]['1W0'][1][2]
	
	dt = 1.0e-6
	
	V1rating = 120
	V2rating = 240
	turns_ratio = V2rating/V1rating
	Rw1 = 0.1
	Rw2 = 0.1*turns_ratio*turns_ratio
	RT1wdg1 = 10000.0
	RT1wdg2 = 10000.0
	M = 0.5
	Ls = 0.0001
	
	if (t_clock <= dt):
	    curr_vector = [0.0, 0.0]
	
	if t_clock>=t1:
	    
	    L_matrix = [[Ls + M, M], [M, (Ls + M)]]
	    R_matrix = [Rw1, Rw2/(turns_ratio*turns_ratio)]
	    V_matrix = [v1meas, v2meas/turns_ratio]
	
	    for count1 in range(len(L_matrix)):
	        if not L_matrix[count1][count1]:
	            for count2 in range(count1 + 1, len(L_matrix)):
	                if L_matrix[count2][count1]:
	                    L_matrix[count1], L_matrix[count2] = L_matrix[count2], L_matrix[count1]
	                    R_matrix[count1], R_matrix[count2] = R_matrix[count2], R_matrix[count1]
	                    V_matrix[count1], V_matrix[count2] = V_matrix[count2], V_matrix[count1]
	                    break
	
	        if L_matrix[count1][count1]:
	            for count2 in range(count1 + 1, len(L_matrix)):
	                if L_matrix[count2][count1]:
	                    comm_factor = L_matrix[count2][count1]/L_matrix[count1][count1]
	                    for count3 in range(len(L_matrix)):
	                        L_matrix[count2][count3] -= L_matrix[count1][count3]*comm_factor
	                    R_matrix[count2] -= R_matrix[count1]*comm_factor
	                    V_matrix[count2] -= V_matrix[count1]*comm_factor
	
	
	    dibydt_matrix = [0.0, 0.0]
	    
	    for count1 in range(len(L_matrix)-1, -1, -1):
	        k_matrix = [0.0, 0.0, 0.0, 0.0]
	        for count2 in range(len(k_matrix)):
	            k_matrix[count2] = V_matrix[count1]
	            for count3 in range(count1 + 1, len(L_matrix)):
	                k_matrix[count2] -= L_matrix[count1][count3]*dibydt_matrix[count3]
	                wdg_current = curr_vector[count1]
	                if count2 == 0:
	                    k_matrix[count2] -= R_matrix[count1]*wdg_current
	                if count2 == 1:
	                    k_matrix[count2] -= R_matrix[count1]*(wdg_current + k_matrix[count2 - 1]*dt/2.0)
	                if count2 == 2:
	                    k_matrix[count2] -= R_matrix[count1]*(wdg_current + k_matrix[count2 - 1]*dt/2.0)
	                if count2 == 3:
	                    k_matrix[count2] -= R_matrix[count1]*(wdg_current + k_matrix[count2 - 1]*dt)
	
	            k_matrix[count2] = k_matrix[count2]/L_matrix[count1][count1]
	        dibydt_matrix[count1] = (k_matrix[0] + k_matrix[1]*2 + k_matrix[2]*2 + k_matrix[3])/6.0
	        curr_vector[count1] += dibydt_matrix[count1]*dt
	
	    VT1wdg1 = v1meas + curr_vector[0]*RT1wdg1
	    VT1wdg2 = v2meas + curr_vector[1]*RT1wdg2/turns_ratio
	    
	    flux = (Ls + M)*curr_vector[0] + M*curr_vector[1]/turns_ratio
	    
	    t1 += dt
	    
	T1_flux = curr_vector[0]

	interface_events[pos] = 0

	if not interface_outputs[pos]['8S0'][1][2]==VT1wdg1:
		interface_events[pos] = 1

	if not interface_outputs[pos]['8U0'][1][2]==VT1wdg2:
		interface_events[pos] = 1

	if not interface_outputs[pos]['1K0'][1][2]==RT1wdg1:
		interface_events[pos] = 1

	if not interface_outputs[pos]['1W0'][1][2]==RT1wdg2:
		interface_events[pos] = 1

	circuit_components['8S0'].control_values[0]=VT1wdg1
	interface_outputs[pos]['8S0'][1][2]=VT1wdg1
	circuit_components['8U0'].control_values[0]=VT1wdg2
	interface_outputs[pos]['8U0'][1][2]=VT1wdg2
	circuit_components['1K0'].control_values[0]=RT1wdg1
	interface_outputs[pos]['1K0'][1][2]=RT1wdg1
	circuit_components['1W0'].control_values[0]=RT1wdg2
	interface_outputs[pos]['1W0'][1][2]=RT1wdg2
	interface_static[pos]['flux']=flux
	interface_static[pos]['curr_vector']=curr_vector
	interface_time[pos]['t1']=t1
	sys_t_events.append(t1)
	interface_variablestore['T1_flux'][0]=T1_flux
	interface_variablestore['VarStor1'][0]=VarStor1
	return

def inv_modulator_func(interface_inputs, interface_outputs, interface_static, interface_time, interface_variablestore,                                 interface_events, circuit_components, pos, t_clock, sys_t_events):
	vloadout=circuit_components['9S2'].op_value
	x_tri=interface_static[pos]['x_tri']
	x_tri_sign=interface_static[pos]['x_tri_sign']
	modsignal=interface_static[pos]['modsignal']
	s1logic=interface_static[pos]['s1logic']
	s2logic=interface_static[pos]['s2logic']
	s3logic=interface_static[pos]['s3logic']
	s4logic=interface_static[pos]['s4logic']
	tcarr=interface_time[pos]['tcarr']
	T1_flux=interface_variablestore['T1_flux'][0]
	VarStor1=interface_variablestore['VarStor1'][0]
	S1inv1gate=interface_outputs[pos]['7F1'][1][2]
	S2inv1gate=interface_outputs[pos]['19F1'][1][2]
	S3inv1gate=interface_outputs[pos]['7L1'][1][2]
	S4inv1gate=interface_outputs[pos]['19L1'][1][2]
	
	dt_carr = 5.0e-7
	carr_freq = 5000.0
	
	
	if t_clock>=tcarr:
	    if (x_tri >= 1.0):
	        x_tri_sign = -1.0
	    
	    if (x_tri <= -1.0):
	        x_tri_sign = 1.0
	    
	    x_tri += x_tri_sign*(4.0*carr_freq)*dt_carr
	    
	    modsignal = 0.97*math.sin(120*math.pi*t_clock)
	    
	    if (x_tri > modsignal):
	        s1logic = 0.0
	        s2logic = 1.0
	        s3logic = 1.0
	        s4logic = 0.0
	    else:
	        s1logic = 1.0
	        s2logic = 0.0
	        s3logic = 0.0
	        s4logic = 1.0
	
	    tcarr += dt_carr
	
	S1inv1gate = s1logic
	S2inv1gate = s2logic
	S3inv1gate = s3logic
	S4inv1gate = s4logic

	interface_events[pos] = 0

	if not interface_outputs[pos]['7F1'][1][2]==S1inv1gate:
		interface_events[pos] = 1

	if not interface_outputs[pos]['19F1'][1][2]==S2inv1gate:
		interface_events[pos] = 1

	if not interface_outputs[pos]['7L1'][1][2]==S3inv1gate:
		interface_events[pos] = 1

	if not interface_outputs[pos]['19L1'][1][2]==S4inv1gate:
		interface_events[pos] = 1

	circuit_components['7F1'].control_values[0]=S1inv1gate
	interface_outputs[pos]['7F1'][1][2]=S1inv1gate
	circuit_components['19F1'].control_values[0]=S2inv1gate
	interface_outputs[pos]['19F1'][1][2]=S2inv1gate
	circuit_components['7L1'].control_values[0]=S3inv1gate
	interface_outputs[pos]['7L1'][1][2]=S3inv1gate
	circuit_components['19L1'].control_values[0]=S4inv1gate
	interface_outputs[pos]['19L1'][1][2]=S4inv1gate
	interface_static[pos]['x_tri']=x_tri
	interface_static[pos]['x_tri_sign']=x_tri_sign
	interface_static[pos]['modsignal']=modsignal
	interface_static[pos]['s1logic']=s1logic
	interface_static[pos]['s2logic']=s2logic
	interface_static[pos]['s3logic']=s3logic
	interface_static[pos]['s4logic']=s4logic
	interface_time[pos]['tcarr']=tcarr
	sys_t_events.append(tcarr)
	interface_variablestore['T1_flux'][0]=T1_flux
	interface_variablestore['VarStor1'][0]=VarStor1
	return

