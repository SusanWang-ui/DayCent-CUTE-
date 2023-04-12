import parm, datetime, msgbox
from numpy import genfromtxt

def read(i,fn, filename): # i: output num
    # Reads yearly measured files

    filen = parm.path_obs + '\\' + filename   
    obsfnam = open(filen, 'r') 
    linestr= obsfnam.readlines() 
    obsfnam.close()
    dum = ' '.join(linestr[0].split())
    data = dum.split(',')
    
    treatment = parm.ISCH
    #treatment = parm.ISCH.replace(parm.Site_name +'_','')
    
    k=0
    for kk in range(len(data)):        
        if data[kk]==treatment:            
            k = kk
            break        
    
    obsdata = genfromtxt(filen,  delimiter=',',skip_header=1)    

    #if fn=='soc_' and k > 0:
    if k > 0:
        parm.obs_val[i] = obsdata[:,k]    
    else:
        parm.error_msg = 'Treatment ' + treatment + ' has no observation data listed in soc_' + parm.Site_name
        msgbox.msg("Error:", parm.error_msg)
        parm.iflg=1
        return

    obs_row_count = obsdata.shape[0]
    # Calendar dates for observed data
    obsdate = [0 for x in range(obs_row_count)]
    for j in range(obs_row_count):
         yr = int(float(obsdata[j, 0]))
         obsdate[j] = datetime.date(yr, 1, 1)
#  it can be non-continuous observations
#         if j > 0:
#              delta = obsdate[j].year - obsdate[j - 1].year
#              if delta > 1:
#                txt = 'Observation data is errornous between ' + str(obsdate[j - 1]) + ' and ' + str(obsdate[j])
#                #parm.error_handle(txt)
#                msgbox.msg("Error", txt)
    parm.obs_date[i] = obsdate[:]

    return   # Susan added

    #Calendar dates for observed data
#    obsdate = [0 for x in range(obs_row_count)]
    for j in range(obs_row_count):
        yr = int(float(obsdata[j,0]))
        obsdate[j] = datetime.date(yr, 1, 1) 
        if j>0:
            delta = obsdate[j].year - obsdate[j-1].year
            if delta>1:
                txt = 'Observation data is errornous between ' + str(obsdate[j-1]) + ' and ' + str(obsdate[j])
                parm.error_handle(txt)

    parm.obs_date[i] = obsdate[:]      
