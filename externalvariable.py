import userclasser as uc
import gv
def uservariable():
    # external variable 1
    #'''
    # we have  an efficency function realised here
    cf = uc.user()
    iload = cf.avg(2,2) #average output current
    vload = cf.avg(2,5) #average output voltage
    isrc = cf.avg(2,3)  #average input current
    vsrc = cf.avg(2,6)  #average output voltage
    kik = ((iload*vload)/(isrc*vsrc)) #calculating efficency
    cf.store(kik) #entering in a special format
    gv.externalvariable = [cf]
    ## '''
    return
