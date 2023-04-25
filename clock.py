import math
import numpy as np
from tqdm import tqdm
import time as timedate
from astropy.time import Time
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def func(x, p):
    a,b = p
    return a*x+b

def residuals(p, y, x):
    return y - func(x, p)

def clockDownsample(mjd,timediff):
    mjds = mjd.mjd

    startMJD = math.ceil(mjds[0])
    endMJD = math.ceil(mjds[-1])
    mjdList = np.arange(startMJD, endMJD)
    mjds_downSamp = []
    timediff_downSamp = []
    timediff_res = []

    for i in tqdm(range(1,endMJD-startMJD)):
    #for i in range(1,endMJD-startMJD):
        #print(i, mjdList[i-1], mjdList[i])
        idx = np.logical_and(mjds < mjdList[i], mjds > mjdList[i-1])
        if (len(mjds[idx]) == 0):
            continue
        else:
            mjd_cut = mjds[idx] 
            timediff_cut = timediff[idx]


            #media_residual = np.median(timediff_cut)
            #mean_residual = np.mean(timediff_cut)
            sampleNum = 12
            #sampleNum = 4
            for j in range(1,sampleNum+1):
                mean_idx = np.logical_and(mjd_cut<(mjdList[i-1]+j*1/sampleNum), mjd_cut>(mjdList[i-1]+(j-1)*1/sampleNum))
                if (len(mjd_cut[mean_idx]) == 0 ):
                    continue
                else:
                    median_mjd = np.median(mjd_cut[mean_idx])
                    median_residual = np.median(timediff_cut[mean_idx])

                    mjds_downSamp.append(median_mjd)
                    timediff_downSamp.append(median_residual)
                    timediff_res.append(np.mean(timediff_cut[mean_idx]) - median_residual)
    mjds_downSamp = np.array(mjds_downSamp)
    timediff_downSamp = np.array(timediff_downSamp)
    timediff_res = np.array(timediff_res)
    return mjds_downSamp, timediff_downSamp, timediff_res



print('haha')


time = []
error = []

# get clock filenames
with open("filelist.txt", 'r') as fw:
    filelist = fw.readlines()

    # load files
    for filename in filelist:
        filename = filename.replace("\n", "")
        print(filename)
        clockdiff = np.loadtxt(filename)
        time += list(clockdiff[:,0])
        error += list(clockdiff[:,1])

time = np.array(time)
error = np.array(error)

# trans to MJD
time_mjd = Time(time, format='unix')

index = (error<1E-3)
time_mjd = time_mjd[index]
error = error[index]

mjd_down, error_down, error_res = clockDownsample(time_mjd,error)
mjd_down = np.array(mjd_down)
error_down = np.array(error_down)

idx = np.isnan(error_down)
mjd_down = mjd_down[~idx]
error_down = error_down[~idx]



print(len(time_mjd), len(error))
print(len(mjd_down), len(error_down), len(error_res))

#plt.plot(time_mjd.mjd ,error, 'k')
#plt.plot(mjd_down, error_down, 'r')
#plt.show()

plt.figure(figsize=(12,9))
idx_res = np.logical_and(error_res<1E-6, error_res>-1E-6)
plt.plot(mjd_down[idx_res], error_res[idx_res]*1E6)
plt.xlabel('MJD')
plt.ylabel('time diff residual(us)')
plt.savefig("timeDiff_res.png",dpi=300)

plt.figure(figsize=(12,9))
plt.plot(time_mjd.mjd, error*1E6,'k', label="origin",lw=2)
plt.plot(mjd_down, error_down*1E6,'r', label="downsample",lw=0.5)
plt.xlabel('MJD')
plt.ylabel('GPS diff (us)')
plt.legend()
#plt.show()
plt.savefig("timeDiff.png",dpi=300)



####################
createData = timedate.strftime('%Y%m%d',timedate.localtime(timedate.time()))

####################
# tempo2
# out put the results
clockHead="#UTC(FAST) UTC(GPS)"
tempo2Clock = 'fast2gps'+createData+'.clk'
print("Write: ", tempo2Clock)
np.savetxt(tempo2Clock, np.array([mjd_down, error_down]).T, header=clockHead,fmt='%.5f %.12f',delimiter=" ", comments='')

####################
#    col      item
#    1-9     MJD 9-1+1 = 9
#   10-21    offset1 (us) 21-10+1 = 12
#   22-33    offset2 (us) 33-22+1 = 12
#   35-35    observatory code 35-35+1 = 1
#   37-37    flag

# tempo
# out put the results
tempoClock = 'time_fast'+createData+'.dat'
clockHead='   MJD       EECO-REF    NIST-REF NS      DATE    COMMENTS\n=========    ========    ======== ==    ========  ========'

data = np.empty([len(mjd_down), 4], dtype=object)
data[:,0] = mjd_down
data[:,1] = 0.0
data[:,2] = error_down * 1E6
data[:,3] = 'k'
print("Write: ", tempoClock)
np.savetxt(tempoClock, data, header=clockHead,fmt='%-8.3f       %-1.3f %11.3f %1s',delimiter=" ", comments='')
#np.savetxt(tempoClock, data, header=clockHead,fmt='%-8.3f % 11.1f % 11.3f % 1s',delimiter=" ", comment    s='')



####################
# tempo2 - all
# out put the results
clockHead="#UTC(FAST) UTC(GPS)"
tempo2Clock = 'fast2gps'+createData+'_origin.clk'
print("Write: ", tempo2Clock)
print(len(time_mjd), len(error))
np.savetxt(tempo2Clock, np.array([time_mjd.mjd, error]).T, header=clockHead,fmt='%.5f %.12f',delimiter=" ", comments='')

####################
# tempo
# out put the results
tempoClock = 'time_fast'+createData+'_origin.dat'
clockHead='   MJD       EECO-REF    NIST-REF NS      DATE    COMMENTS\n=========    ========    ======== ==    ========  ========'

data = np.empty([len(time_mjd.mjd), 4], dtype=object)
data[:,0] = time_mjd.mjd
data[:,1] = 0.0
data[:,2] = error * 1E6
data[:,3] = 'k'
print("Write: ", tempoClock)
np.savetxt(tempoClock, data, header=clockHead,fmt=' %8.3f      %-1.3f %11.3f %1s',delimiter=" ", comments='')

