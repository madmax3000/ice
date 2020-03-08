import pandas as pd
import globalfile as gf
import function as fu
import csv


class user:
    def __init__(self):
        self.value = 0.1  # the value of external variable is stored here
        self.meterno = 1  # thee meter value is stored here
        self.rowno = 1  # the row no is stored
        self.paramsfileno = 1  # the params file value is used here
        self.outputfileno = 1  # the outfile details are used here

    def element(self, paramsfileno, rowno):
        '''
        f = pd.read_csv(gf.paramsarray[paramsfileno], header=None, index_col=False)
        c  = f.iloc[meterno, 3]
        f.to_csv(gf.paramsarray[paramsfileno], sep=',', header=None, index_col=False, )
        return c
        '''
        with open(gf.paramsarray[paramsfileno-1], 'r') as f:
            reader = csv.reader(f)  # read parameter file
            urlist = list(reader)  # converting parameter file as a list
        c = float(urlist[rowno-1][3])  # assigning valve bacck
        new = pd.DataFrame(urlist)  # rewriting the parameters back
        new.to_csv(gf.paramsarray[paramsfileno-1], sep=',', header=False, index=False, )
        return c

    def avg(self, outputfileno, meterno):
        return fu.avg(outputfileno-1, meterno-1)  # the avg is computed

    def rms(self, outputfileno, meterno):
        return fu.rms(outputfileno-1, meterno-1)

    def thd(self, outputfileno, meterno):
        return fu.thd(outputfileno-1, meterno-1)

    def peak(self, outputfileno, meterno):
        return fu.peak(outputfileno-1, meterno-1)

    def ripple(self, outputfileno, meterno):
        return fu.ripple(outputfileno-1, meterno-1)

    def mov_avg_final(self, outputfileno, meterno):
        return fu.moving_avg(outputfileno-1, meterno-1)

    def store(self, value):
        self.value = value
        return
    def __str__(self):
        return str(self.value)

