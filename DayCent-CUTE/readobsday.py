import parm, datetime, calendar
from numpy import genfromtxt
import msgbox

def read(i,fn,filename):
    #Reads daily measured files and selects requiered data
    yr, dayofyr = 0,0
    
    filen = parm.path_obs + '\\' + filename
    obsdata = genfromtxt(filen,  delimiter=',', skip_header=1)

    if fn=='n2o_' or fn=='ch4_':
        parm.obs_val[i] = obsdata[:,2]         # column 3 is N2O or CH4
    
    #Count the total number of days
    obs_row_count = obsdata.shape[0]
                
    #Calendar dates for observed data
    obsdays = [0 for x in range(obs_row_count)] 
    for j in range(obs_row_count):
        yr = int(float(obsdata[j,0]))                
        dayofyr = int(float(obsdata[j,1]))
        obsdays[j] = datetime.date(yr, 1, 1) + datetime.timedelta(dayofyr - 1) 
    
    parm.obs_date[i] = obsdays    