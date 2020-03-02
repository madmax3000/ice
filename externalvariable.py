import userclasser as uc
import gv
def uservariable():
    # external variable 1
    '''
    cf = uc.user()
    ap = cf.element(1,0)
    ap1 = cf.element(1,1)
    m=0.3
    kik=m*(ap*ap1)
    cf.store(kik)   # a sample external variable
    print(cf.value)

    # external variable 2
    cf1 = uc.user()
    ap2 = cf1.element(1,3)
    ap3 = cf1.element(1,2)
    m3=0.3
    ou1 = cf1.peak(1,3)
    kiku=(m3*(ap2*ap3)/ou1)
    cf1.store(kiku) # a second external variable
    print(cf1)
    gv.externalvariable=[cf,cf1]
    '''
    cf = uc.user()
    ap = cf.element(3, 8)
    ap1 = cf.element(3, 9)
    m = 0.3
    kik = m * (ap * ap1)
    cf.store(kik)
    gv.externalvariable = [cf]
    return
