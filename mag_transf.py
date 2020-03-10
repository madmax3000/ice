import math
import globalfile as gf

dt = 1.0e-6

V1rating = 120.0
V2rating = 240.0
turns_ratio = V2rating/V1rating
Rw1 = 0.1
Rw2 = 0.1*turns_ratio*turns_ratio
RT1wdg1 = 1000000.0
RT1wdg2 = 1000000.0
M = 0.5
Ls = gf.controlvariable[0]
print(Ls)

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

    VT1wdg1 = v1meas - curr_vector[0]*RT1wdg1
    VT1wdg2 = v2meas - curr_vector[1]*RT1wdg2/turns_ratio
    
    flux = (Ls + M)*curr_vector[0] + M*curr_vector[1]/turns_ratio
    
    t1 += dt
    
T1_flux = curr_vector[0]
