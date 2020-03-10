import userclasser as uc
import gv
def uservariable():
    # external variable 1
    #'''
    # we have  an efficency function realised here
    cf = uc.user()
    iload = cf.avg(2,2)
    vload = cf.avg(2,5)
    isrc = cf.avg(2,3)
    vsrc = cf.avg(2,6)
    kik = ((iload*vload)/(isrc*vsrc))
    cf.store(kik-30)
    gv.externalvariable = [cf]
    ## '''
    return
