import parm, os, subprocess, math
import numpy as np

def run():
    import data_pairing, statistics_1
    import DayCentFIX100, DayCentSitepar, DayCentOutputF, DayCentSite, DayCentCULT100

    # Update DayCent files
    if parm.iparm>0:
        DayCentFIX100.update()
        if parm.iflg==1: return
    if parm.isitepar > 0:
        DayCentSitepar.update()
        if parm.iflg==1: return
    if parm.isite100 > 0:
        DayCentSite.update()
        if parm.iflg==1: return
    if parm.cult100 > 0:
        DayCentCULT100.update()
        if parm.iflg==1: return

    # Run DayCent
    os.chdir(parm.path_TxtWork)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    fbinname = parm.ISCH + ".bin"
    if os.path.exists(fbinname):
        os.remove(fbinname)    
    if len(parm.IBIN) > 0:
        command_line1 = 'DDcentEVI.exe -s {} -n {} -e {}'.format(parm.ISCH, parm.ISCH, parm.IBIN)
    else:
        command_line1 = 'DDcentEVI.exe -s {} -n {}'.format(parm.ISCH, parm.ISCH)
    command_line2 = 'DDlist100.exe {} {} {}'.format(parm.ISCH, parm.ISCH, 'outvars.txt')
    retcode = subprocess.Popen(command_line1, startupinfo=startupinfo, creationflags=0x08000000)
    retcode.wait()
    retcode = subprocess.Popen(command_line2, startupinfo=startupinfo,
                               creationflags=0x08000000)  # This will create DayCent .lis output file
    retcode.wait()

    # Collect DayCent output
    DayCentOutputF.select_file()
    if parm.iflg == 1: return

    # Arrange paired dataset for pred-obs comparison
    data_pairing.dataPair()
    if parm.iflg == 1: return

    # Calculate OF
    parm.cur_test_OF = 0
    sum_weight = 0
    for i in range(len(parm.DayCent_outputFile)):
        sum_weight = sum_weight + parm.of_weight[i]

    if parm.obs_yld_type == '9999':
        if len(parm.pairpCal) < 6:
            ofnew = (np.mean(parm.pairoCal) - np.mean(parm.pairpCal)) / np.mean(parm.pairoCal) * 100  # percent bias
        else:
            statistics_1.performance_indicators(parm.pairpCal, parm.pairoCal)
            ofnew = 0
            if parm.dds_stat.upper() == "F(NSE-PBIAS)":
                ofnew = math.sqrt((1 - parm.nse) ** 2 + (math.fabs(parm.re) / 100 + 0.5) ** 2)
            elif parm.dds_stat.upper() == "R2":
                ofnew = 1 - parm.r2
            elif parm.dds_stat.upper() == "RMSE":
                ofnew = parm.rmse
            elif parm.dds_stat.upper() == "ABSOLUTE ERROR":
                ofnew = parm.bias
            elif parm.dds_stat.upper() == "PBIAS":
                ofnew = math.fabs(parm.re)
            elif parm.dds_stat.upper() == "NSE":
                ofnew = 1 - parm.nse
        parm.cur_test_OF = ofnew
    else:
        for i in range(len(parm.DayCent_outputFile)):
            parm.of_weight[i] = parm.of_weight[i] / sum_weight
            statistics_1.performance_indicators(parm.pairpCal[i], parm.pairoCal[i])
            ofnew = 0
            if parm.dds_stat.upper() == "F(NSE-PBIAS)":
                ofnew = math.sqrt((1 - parm.nse) ** 2 + (math.fabs(parm.re) / 100 + 0.5) ** 2)
            elif parm.dds_stat.upper() == "R2":
                ofnew = 1 - parm.r2
            elif parm.dds_stat.upper() == "RMSE":
                ofnew = parm.rmse
            elif parm.dds_stat.upper() == "ABSOLUTE ERROR":
                ofnew = parm.bias
            elif parm.dds_stat.upper() == "PBIAS":
                ofnew = math.fabs(parm.re)
            elif parm.dds_stat.upper() == "NSE":
                ofnew = 1 - parm.nse

            parm.cur_test_OF = parm.cur_test_OF + ofnew * parm.of_weight[i]