import os
import argparse
import numpy as np
from pint.observatory import clock_file
#from clock_file import *

def help_doc():
    print( 
    """
>      OBS_NIST FILE (typically 'time.dat')
>      
>      
>      This file contains clock offsets between observatory clocks (to which
>      TOAs are referenced) and UTC(NIST).
>      
>      The first two lines of this file are ignored.  Subsequent lines have
>      the format:
>      
>          col      item
>          1-9     MJD
>         10-21    offset1 (us)
>         22-33    offset2 (us)
>         35-35    observatory code
>         37-37    flag
>      
>      The difference offset1-offset2 is ObservatoryTime-UTC(NIST).  If the
>      flag is ' ' (blank), offsets from the two entries closest to the
>      target MJD are linearly interpolated.  If the flag is 'f', the closest
>      entry to the target MJD is used without interpolation.
>      
>      Clock offsets from a given observatory must be in chronological order,
>      but offsets from different observatories may be intermixed.
    """)

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
    print("MJD length", len(mjds))
    clk1 = [str(i).rjust(12) for i in clk1]
    print("clk1 length", len(clk1))
    clk2 = [str(i.value).rjust(12) for i in clk2]
    print("clk2 length", len(clk2))
    csite = "k".rjust(2)
    with open(filename,"w") as fn:
        fn.write('   MJD       EECO-REF    NIST-REF NS      DATE    COMMENTS'+'\n')
        fn.write('=========    ========    ======== ==    ========  ========'+'\n')
        for i in range(nMJD):
            outPutLine = mjds[i] + clk1[i] + clk2[i] + csite+'\n' 
            fn.write(outPutLine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transit the clock correction files from TMEPO2 format to TEMPO format.")
    parser.add_argument("-t", "--transit", help='Usage: python clockFileFormatChange.py -t', default=0, action="count")
    args = parser.parse_args()

    if args.transit == 0:
        help_doc()

    #python clockFileFormatChange.py -t then start transit
    if args.transit == 1:
        clockFile_tempo2 = os.getenv('TEMPO2')+'/clock/fast2gps.clk'
        print("#"*50)
        cf = clock_file.ClockFile.read(clockFile_tempo2)
        print("load clock: ", clockFile_tempo2)
        print(cf.time)
        print(cf.clock)
        
        # out the fast tempo clock file
        tempo2_to_tempo1_clock_file("time_fast.dat", cf.time, clk2=cf.clock)
    
