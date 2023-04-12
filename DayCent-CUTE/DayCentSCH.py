import parm, datetime
import msgbox

def read():
    idate=[]
    # read .SCH to initiate the program
    fnam = parm.path_TxtWork + '\\'+parm.ISCH+'.sch'
    try:
        parm.ScheduleFile = open(fnam, 'r')
    except:
        # Print error message and exit
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return 

    lnum = 1
    for txtline in parm.ScheduleFile:
        dum = ' '.join(txtline.split())
        data = dum.split(' ')
        if lnum == 1:
            parm.txt_beginYr = int(float(data[0]))   # Starting year of simulation
        elif lnum == 2:
            parm.txt_endYr = int(float(data[0]))     # Last year of simulation
        elif lnum == 3:
            parm.site_fn = data[0]       # site file name 
        elif lnum == 21:
            parm.txt_outputSYr = int(float(data[0]))  # Output starting year
            if parm.txt_outputSYr < parm.txt_beginYr:
                parm.error_msg = "Output starting year is before simulation starting year."
                msgbox.msg("Error ", parm.error_msg)
                return
            break
        lnum += 1
            
    parm.ScheduleFile.close()
    if parm.reset_config_status == 1: return

#   a = datetime.date(parm.txt_beginYr, 1, 1)
    a = datetime.date(parm.txt_outputSYr, 1, 1)
    b = datetime.date(parm.txt_endYr, 12, 31)

    for i in range(0, len(parm.DayCent_outputFile)):
        # for using Yearly (or aggregated yearly) DayCent output/s (Sensitivity analysis will use Yearly output)
        if parm.obs_dt[i].upper() == 'DAILY':
            day_count = (b-a).days+1
            idate = [0 for x in range(day_count)] 
            idate[0] = a
            for ii in range(1,day_count):
                idate[ii] = idate[ii-1] + datetime.timedelta(days=1)

        elif parm.obs_dt[i].upper() == 'MONTHLY':     
            day_count = (b.year - a.year) * 12 + b.month - a.month + 1
            idate = [0 for x in range(day_count)] 
            idate[0] = a
            for ii in range(1,day_count):
                month = idate[0].month + ii - 1
                year = idate[0].year + month // 12
                month = month % 12 + 1
                idate[ii] = datetime.date(year, month, 1)

        else: # YEARLY 
            day_count = (b.year - a.year)  + 1
            idate = [0 for x in range(day_count)] 
            idate[0] = a
            for ii in range(1,day_count):
                idate[ii] = addYears(idate[ii-1],1)
        
        #   year_count = (b.year - a.year) + 1
        #   idate = [0 for x in range(year_count)]
        #   idate[0] = a
        #   for ii in range(1, year_count):
        #        idate[ii] = addYears(idate[ii - 1], 1)

        parm.pred_date[i] = idate
        parm.start_pred[i] = idate[0]
        parm.end_pred[i] = idate[len(idate) - 1]

    # Check periods of simulation, calibration, and validation
        if parm.SA_orCal == 0: # for calibration
            if parm.end_cal < parm.start_pred[i] or parm.start_cal > parm.end_pred[i]:
                parm.error_msg = 'Calibration period is not within the simulation period!!'
                msgbox.msg("Warning",parm.error_msg)
                parm.iflg=1; return

            if parm.flg_validation!=0:
                if parm.end_val < parm.start_pred[i] or parm.start_val > parm.end_pred[i]:
                    parm.error_msg = 'Validation period is not within the simulation period!!'
                    msgbox.msg("Warning",parm.error_msg)
                    parm.iflg=1; return


def addYears(d, years):
    try:
# Return same day of the current year
        return d.replace(year = d.year + years)
    except ValueError:
# If not same day, it will return other, i.e.  February 29 to March 1 etc.
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
            
