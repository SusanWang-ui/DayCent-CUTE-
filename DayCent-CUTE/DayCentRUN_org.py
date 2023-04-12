import parm, subprocess
import msgbox


def read():
    fnam = parm.path_TxtWork + '\DayCentRUN.DAT'
    try:
        parm.fnam1 = open(fnam, 'r')
    except:
        # Print error message and exit
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg = 1;
        return

    lnum = 1
    for txtline in parm.fnam1:
        txtline = txtline.split()
        if lnum == 1:
            parm.Site_name = txtline[0]  # Name for DayCent run
            parm.ISCH = txtline[1]  # .sch file name only
            if len(txtline) == 4:
                parm.IBIN = txtline[3]  # .bin of previous simulation file (file name only) to initialize the model
            lnum += 1
        else:
            break
    parm.fnam1.close()


def SingleBatchRun():
    import itertools
    import parm, os

    os.chdir(parm.path_TxtWork)
    fnam = parm.path_TxtWork + '\DayCentRUN.DAT'

    # Write headers   # if have a template file, then no need to rewrite
    #    txt = str("{:>5}".format('Run#')) + str("{:>16}".format('Output')) + str("{:>13}".format('Performance'))
    #    txt = txt + str("{:>26}".format('<-Predicted vs. Observed values->')) + '\n'
    #    f_modPerfout.writelines(txt)

    output_perf()
    with open(fnam) as f:
        for txtline in itertools.islice(f, 1, None):  # start=1, stop = None
            txtline = txtline.split()
            if len(txtline) == 0:
                parm.fnam1.close()
                parm.iflg = 1
                return
            else:
                parm.DayCentRun_name = txtline[0]  # Name for DayCent run
                parm.ISCH = txtline[1]  # .sch file name only
                if len(txtline) == 4:
                    parm.IBIN = txtline[3]  # .bin of previous simulation file (file name only) to initialize the model
                else:
                    parm.IBIN =""
                # Run DayCent
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW              
                fbinname = parm.ISCH + ".bin"
                if os.path.exists(fbinname): os.remove(fbinname)
                if len(parm.IBIN) > 0:
                    command_line1 = 'DD17centEVI.exe -s {} -n {} -e {}'.format(parm.ISCH, parm.ISCH, parm.IBIN)
                else:
                    command_line1 = 'DD17centEVI.exe -s {} -n {}'.format(parm.ISCH, parm.ISCH)
                retcode = subprocess.Popen(command_line1, startupinfo=startupinfo, creationflags=0x08000000)
                command_line2 = 'DD17list100.exe {} {} {}'.format(parm.ISCH, parm.ISCH, 'outvars.txt')
                retcode.wait()
                retcode = subprocess.Popen(command_line2, startupinfo=startupinfo,
                               creationflags=0x08000000)  # This will create DayCent .lis output file
                retcode.wait()
                output_perf()                    


def output_perf():
    import Single_BatchRun_data_pairing, statistics_1, DayCentOutputF, ObsData

    # Collect DayCent output
    DayCentOutputF.select_file()  

    ObsData.read()
    for i in range(len(parm.DayCent_var)):    
      if parm.obs_date[i] == 0:  # no observed data
        output(i)        
      else:
        fname = parm.path_proj + '\\SingleBatch_modPerf.out'
        f_modPerfout = open(fname, 'a')
        # Arrange paired dataset for pred-obs comparison
        Single_BatchRun_data_pairing.run(i)
        if parm.iflg==1: return
        Single_BatchRun_data_pairing.dataPair(i)
        if parm.iflg == 1: return

        #for i in range(len(parm.DayCent_outputFile)):
        statistics_1.performance_indicators(parm.pairpCal[i], parm.pairoCal[i])
        txt = str("{:>14}".format(parm.ISCH))
        if parm.obs_date[i] == 9999:
            txt = txt + "{:>9}".format(parm.obs_dt[i]) + "{:10.3f}".format(parm.re) + '%10.3f' % parm.pairpCal[i]
        else:
            txt = txt + str("{:>10}".format(parm.DayCent_var[i])) + "{:10.3f}".format(parm.bias1)+"{:10.3f}".format(-parm.re)  # -parm.re is the Percent error PBIAS (parm.meanpr-meanob) / meanob * 100
            # only paired values for calibration period
            for j in range(len(parm.pairpCal[i])):
                txt = txt + '%10.3f' % parm.pairpCal[i][j] + '%10.3f' % parm.pairoCal[i][j]
        txt = txt + '\n'
        f_modPerfout.writelines(txt)
        f_modPerfout.flush()
        f_modPerfout.close()        
    return

def output(i):
    fname = parm.path_proj + '\\SingleBatchRun.out'
    f_DayCentout = open(fname, 'a')

    # Write headers   # if have saved in a template file, then no need to rewrite
#    txt = str("{:>5}".format('Run#')) + str("{:>16}".format('Output')) + str("{:>20}".format('Predicted_values-->')) + '\n'
#    f_DayCentout.writelines(txt)
    
    txt = str("{:>13}".format(parm.ISCH)) + str("{:>10}".format(parm.DayCent_var[i]))
    if parm.start_cal != 0:
       for j in range(len(parm.pred_val[i])):
            txt = txt + '%10.3f' % parm.pred_val[i][j]
    txt = txt + '\n'
    f_DayCentout.writelines(txt)
    f_DayCentout.flush()
    f_DayCentout.close()
