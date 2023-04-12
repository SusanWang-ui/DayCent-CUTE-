import parm, math, datetime
import numpy as np
import msgbox
#import calendar

def select_file():
    # Read DayCent output values from .LIS file
    LISnum = 0
    YearSummaryOut = 0
    HarvOut = 0
    DlySummary = 0
    for i in range(0,len(parm.DayCent_outputFile)):   # outputFile, such as .LIS, .LIS,
        if parm.DayCent_outputFile[i]=='LIS':         # Select .LIS file
           LISnum += 1
        elif parm.DayCent_outputFile[i]=='YsumaryOUT':
           YearSummaryOut +=1
        elif parm.DayCent_outputFile[i]=='harvestCSV':
           HarvOut +=1
        elif parm.DayCent_outputFile[i]=='DsummaryOUT':
           DlySummary +=1

    if LISnum >= 1:
        LISread(LISnum)        # read all selected variables in the .LIS file
    if YearSummaryOut >= 1:
        Ysumread(YearSummaryOut)
    if HarvOut >= 1:
        harvestRead(HarvOut)
    if DlySummary >= 1:
        summaryRead(DlySummary)

def summaryRead(DlySummary):
    # This module reads DayCent summary.out file.
    yr, dayofyr = 0, 0

    fnam = parm.path_TxtWork + '\\summary.out'
    try:
        lis_data = np.genfromtxt(fnam,delimiter='', skip_header=1)        # lis_data[row,column]
        #Count the total number of days        
    except:
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    date_row_count = lis_data.shape[0]        
    lis_date = [0 for x in range(date_row_count)] 
    for j in range(date_row_count):
        yr = int(float(lis_data[j,0]))                
        dayofyr = int(lis_data[j,1]) 
        lis_date[j] = datetime.date(yr, 1, 1) + datetime.timedelta(dayofyr - 1)

    for i in range(0,len(parm.DayCent_outputFile)):  
        if DlySummary > 0:        
            if parm.DayCent_var[i]=="DLY-N2O":               #  g N/ha/day
                parm.pred_val[i] = lis_data[:,5]        #                 
                DlySummary -= 1
            elif parm.DayCent_var[i]=="DLY-CH4":      #  g C/ha/day
                parm.pred_val[i] = lis_data[:,7]            
                DlySummary -= 1                
            parm.pred_datea[i] = lis_date                    
        else:
            break

def LISread(LISnum):
    # This module reads DayCent output *.lis file.
    fnam = parm.path_TxtWork + '\\' + parm.ISCH + '.lis'
    try:
        # The column names are in the second row, and you'll want to skip the output from the equilibrium run 
        #   and retrieve only the years you want to evaluate.
        lis_data = np.genfromtxt(fnam,delimiter='', skip_header=3)        # lis_data[row,column]
        k = 0
        for j in range(0, len(lis_data[:, 0])):
            if math.floor(lis_data[j, 0]) == parm.txt_outputSYr:
                k = j  # row in lis_data to start to read
                break  # terminate this innermost loop only
        #if k == 0:
        #    return
    except: 
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    parm.iflg = 0
    lis_data = np.genfromtxt(fnam, delimiter='', skip_header = k + 3)  # lis_data[row,column]

    for i in range(0,len(parm.DayCent_outputFile)):  # len(parm.DayCent_outputFile) is the same as len(parm.DayCent_var); DayCent output variables to evaluate
        if LISnum > 0:        
            var1=[]
            lis_date=[]
            if parm.DayCent_var[i]=="LIS-SOMSC":                  #  g C/m2
                var1 = lis_data[:,2]        # column 3 is SOMSC
                lis_date = lis_data[:, 0]  # The time column in DayCent .LIS file
                LISnum -= 1
            elif parm.DayCent_var[i]=="LIS-SOMTC":
                var1 = lis_data[:,3]
                lis_date = lis_data[:, 0]  # The time column in DayCent .LIS file
                LISnum -= 1

            ndata = len(parm.pred_date[i])
            parm.pred_datea[i] = parm.pred_date[i]
            ival = [0 for x in range(ndata)]
            idt = 0
            sum = 0
            for j in range(1,len(var1)):  # the first number is the initial value of SOC 
                sum = sum + var1[j]
                # the monthly time values in the *.bin (.lis) files are shifted by 1/12 such that for year 1994: Jan is 1994.08 and Dec is 1995 (which is 1994+12/12)
                #  using mean for SOC in the year (reducing fluctuation)
                if j>10 and lis_date[j] == math.ceil(lis_date[j-1]):
                    ival[idt] = sum / 12
                    idt += 1
                    sum = 0
            parm.pred_val[i] = ival[:]          
        else:
            break

def Ysumread(YearSummaryOut):
    # This module reads DayCent year_summary.out file.
    fnam = parm.path_TxtWork + '\\year_summary.out'
    try:
        lis_data = np.genfromtxt(fnam,delimiter='', skip_header=1)        # lis_data[row,column]
    except:
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    for i in range(0,len(parm.DayCent_outputFile)):  # len(parm.DayCent_outputFile) is the same as len(parm.DayCent_var); DayCent output variables to evaluate
        if YearSummaryOut > 0:
            if parm.DayCent_var[i]=="YLY-N2O":                  #  g N/m2/yr
                parm.pred_val[i] = lis_data[:,1]
                YearSummaryOut -= 1
            elif parm.DayCent_var[i]=="YLY-CH4":                #  g C/m2/yr
                parm.pred_val[i] = lis_data[:, 4]
                YearSummaryOut -= 1

            parm.pred_datea[i] = parm.pred_date[i]
        else:
            break

def harvestRead(HarvOut) :
    # This module reads DayCent year_summary.out file.
    fnam = parm.path_TxtWork + '\\harvest.csv'
    try:
        lis_data = np.genfromtxt(fnam,delimiter=',', skip_header=1)        # lis_data[row,column]
        k = 0
        for j in range(0, len(lis_data[:, 0])):
            if math.floor(lis_data[j, 0]) == parm.txt_outputSYr:
                k = j  # row in lis_data to start to read
                break  # terminate this innermost loop only
        #if k == 0:
        #    return
    except:
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    lis_data = np.genfromtxt(fnam,delimiter=',', skip_header = k + 1)   # lis_data[row,column]

    for i in range(0,len(parm.DayCent_outputFile)):
        if HarvOut > 0:
            if parm.DayCent_var[i]=="harvest-cgrain":                  #  g C m-2 harvest-1)
                parm.pred_val[i] = lis_data[:,6]
                HarvOut -= 1

            parm.pred_datea[i] = parm.pred_date[i]

        else:
            break