import userclasser as uc
import gv
def uservariable():
    # external variable 1
    #'''
    # we have  an efficency function realised here
    cf = uc.user()
    iload = abs(cf.avg(2,3)) #average output current
    vload = abs(cf.avg(2,7)) #average output voltage
    isrc = abs(cf.rms(2,2))  #average input current
    vsrc = abs(cf.avg(2,6))  #average output voltage
    kik = ((iload*vload)/(isrc*vsrc)) #calculating efficency
    cf.store(kik*100) #entering in a special format
    gv.externalvariable = [cf]
    ## '''
    return
