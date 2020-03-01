import math

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
