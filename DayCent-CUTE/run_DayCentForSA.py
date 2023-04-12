import parm, os, subprocess

def run(runID):
    import DayCentFIX100, SA_aggregate, DayCentOutputF, DayCentSitepar, DayCentSite #, data_pairing

    # Update DayCent files: right now only working on FIX.100
    if parm.iparm>0:
        DayCentFIX100.update()
        if parm.iflg==1: return
    if parm.isitepar > 0:
        DayCentSitepar.update()
        if parm.iflg==1: return
    if parm.isite100 > 0:
        DayCentSite.update()
        if parm.iflg==1: return
#    if parm.icrop > 0:
#        APEXCROP.update()
#        if parm.iflg==1: return

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
    if parm.iflg==1: return                 
#    APEXACY.select_file()
#    if parm.iflg==1: return

    #get the simulation period
    if parm.iflg==1: return

    SA_aggregate.SAaggregate_data(runID)
    if parm.iflg==1: return                 
#    APEXACY.select_file()    
#    acyread()

