import os
import numpy as np
from pint.observatory import clock_file
#from clock_file import *

def tempo2_to_tempo1_clock_file(filename, mjd, clk1=None, clk2=None):
    """
    change the given tempo2 clock to tempo1 format
    For FAST
       MJD       EECO-REF    NIST-REF NS      DATE    COMMENTS
=========    ========    ======== ==    ========  ========
 45302.81     818.800       2.110 3 f  29-NOV-82  | AW -- A. Wolszczan had data
 #UTC(FAST) UTC(GPS)
57960.24074  0.000002427

    """
    # out put format:
    #  0 - 9   MJD        # 9
    #  9 - 21  clkcorr1   # 12
    # 21 - 33  clkcorr2   # 12
    #   34     site       #

    nMJD = len(mjd)     
    outPutLine = []

    if clk1 is None:
        clk1 = np.zeros(nMJD)

    if clk2 is None:
        clk2 = np.zeros(nMJD)
    
    #  0 - 9   MJD
    #  9 - 21  clkcorr1
    # 21 - 33  clkcorr2
    #   34     site    "FAST is k and FA"
    mjds = [str(i).rjust(9) for i in mjd]
    clk1 = [str(i).rjust(12) for i in clk1]
    clk2 = [str(i.value).rjust(12) for i in clk2]
    csite = "k".rjust(2)
    with open(filename,"w") as fn:
        fn.write('   MJD       EECO-REF    NIST-REF NS      DATE    COMMENTS'+'\n')
        fn.write('=========    ========    ======== ==    ========  ========'+'\n')
        for i in range(nMJD):
            outPutLine = mjds[i] + clk1[i] + clk2[i] + csite+'\n' 
            fn.write(outPutLine)


clockFile_tempo1 = os.getenv('TEMPO')+'/clock/time_ao.dat'
clockFile_tempo2 = os.getenv('TEMPO2')+'/clock/fast2gps.clk'

cf = clock_file.ClockFile.read(clockFile_tempo1)
print("load clock: ", clockFile_tempo1)
print(cf.time)
print(cf.clock)

print("#"*50)

cf = clock_file.ClockFile.read(clockFile_tempo2)
print("load clock: ", clockFile_tempo2)
print(cf.time)
print(cf.clock)

# out the fast tempo clock file
tempo2_to_tempo1_clock_file("time_fast.dat", cf.time, clk2=cf.clock)
