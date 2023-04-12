import parm

#Identify DayCent input files to update
def update():
    j=0
    parm.iparm=0
    parm.isitepar=0
    parm.isite100=0
    parm.icrop100=0
    parm.cult100=0
    for j in range(len(parm.par_name)):
        if parm.par_filename[j].upper() == 'PARM':
            parm.iparm = parm.iparm + 1
        elif parm.par_filename[j].upper()=='SITEPAR':
            parm.isitepar = parm.isitepar + 1
        elif parm.par_filename[j].upper()=='SITE':  
            if len(parm.IBIN) == 0:  
                parm.isite100 = parm.isite100 + 1
        elif parm.par_filename[j].upper()=='CULT':    
            parm.cult100 = parm.cult100 + 1
        elif parm.par_filename[j].upper()=='CROP':    # no update for crop.100; not worked on it yet
            parm.icrop = parm.icrop100 + 1
        