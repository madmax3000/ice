sw_freq = 85000.00
if t_clock >= t1:

    if c==1:
        S1_gate = 1.0
        S4_gate = 1.0
        S2_gate = 0.0
        S3_gate = 0.0
        c=0
        #t1 = t1 + (1 / sw_freq) * (0.5)
        print(" switching is good1\n")
    else:
        S1_gate = 0.0
        S4_gate = 0.0
        S2_gate = 1.0
        S3_gate = 1.0
        c=1
        #t1 = t1 + (1 / sw_freq)*(0.5)
        print(" switching is good2\n")
    t1 = t1 + (1 / sw_freq)
print("tclock : ",t_clock)
print("t1 : ", t1)
S1inv1gate = s1logic
S2inv1gate = s2logic
S3inv1gate = s3logic
S4inv1gate = s4logic
