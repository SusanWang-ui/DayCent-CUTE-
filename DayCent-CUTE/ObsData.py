import parm, os
import msgbox

# identify which observed data files to use
def read():

    filelist = []   
    fn = []
    parm.obs_val = [0 for x in range(len(parm.DayCent_var))]
    parm.obs_date = [0 for x in range(len(parm.DayCent_var))]
    parm.start_obs = [0 for x in range(len(parm.DayCent_var))]
    parm.end_obs = [0 for x in range(len(parm.DayCent_var))]

    # Verify if obs files exist
    for file in os.listdir(parm.path_obs):
        if file.endswith(".csv"):
            filelist.append(file)

    for i in range(len(parm.DayCent_var)):
        if parm.DayCent_var[i] == "LIS-SOMSC":    # or parm.DayCent_var[i] == "LIS-SOMTC":
            fn = 'soc_'
            readfn(i,fn,filelist)
        elif parm.DayCent_var[i] == "DLY-N2O":
            fn = 'n2o_'
            readfn(i,fn,filelist)
        elif parm.DayCent_var[i] == "DLY-CH4":
            fn = 'ch4_'
            readfn(i,fn,filelist)
        else:
            parm.error_msg = parm.DayCent_var[i] + ' has not been coded for calibration yet.'
            msgbox.msg("Error ", parm.error_msg)
            parm.iflg=1; return

        if parm.iflg ==0:
            #Start/ending date                
            parm.start_obs[i] = parm.obs_date[i][0]
            parm.end_obs[i] = parm.obs_date[i][len(parm.obs_date[i])-1]
                    

def readfn(i,fn,filelist):   
    import readobsday
    import readobsmonth
    import readobsyear
    if parm.obs_dt[i].upper() == 'DAILY':
        filename = fn + 'dly_' + parm.ISCH + '.csv'
        if not filename in filelist:
            if parm.SA_orCal == 0:
                parm.error_msg = filename + ' is not found'
                msgbox.msg("Error ", parm.error_msg)
            parm.iflg=1; return    
        else:
            parm.iflg=0
            readobsday.read(i,fn,filename)

    elif parm.obs_dt[i].upper() == 'MONTHLY':
        filename = fn + 'monthly' + parm.ISCH + '.csv'
        if not filename in filelist:
            if parm.SA_orCal == 0:
                parm.error_msg = filename + ' is not found'
                msgbox.msg("Error ", parm.error_msg)
            parm.iflg=1; return
        else:
            parm.iflg=0
            readobsmonth.read(i,fn)

    elif parm.obs_dt[i].upper() == 'YEARLY':
        filename = fn + parm.Site_name + '.csv'
        if not filename in filelist:
            if parm.SA_orCal == 0:         # for Single or Batch Run, it is ok without observed data, selected output will be printed in SingleBatchRun.out
                parm.error_msg = filename + ' is not found'
                msgbox.msg("Error ", parm.error_msg)              
            parm.iflg=1; return
        else:
            parm.iflg=0
            readobsyear.read(i, fn, filename)
