import os, parm
import msgbox
import main_prog

def update():
    #This module updates DayCent outvars.txt file 
       
    flis=0
#    frch=0
#    facy=0
#    fdws=0
    for i in range(0,len(parm.DayCent_outputs)):
        if parm.DayCent_output[i]=='LIS': flis=1
#        if parm.DayCent_output[i]=='RCH': frch=1
#        if parm.DayCent_output[i]=='ACY': facy=1
        
#    if len(parm.cs_name)>0 and parm.cs_on==1:
#        if parm.cs_name[i].lower()=='rto_bf' or parm.cs_name[i].lower()=='pet': fdws=1

    fnam = parm.path_TxtWork + '/' + parm.fnam_outvars
    try:
        parm.fnam1 = open(fnam, 'r+')
    except:
        # Print error message and exit
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    try:
         parm.fnam2 = open(parm.path_TxtWork + 'temp.txt','w') # temp file
    except:
        #Print error message and exit
        parm.error_msg = "An error was occurred while \n creating temp.tmp for DayCent outvars.txt file."
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    # Print options that correspond to each erosion method
    #        MUST    AOF    USLE   MUSS   MUSL  MUSI   RUSL   RUS2
    txt = ['  30','  28','  26','  29','  27',' 124',' 107','  31']
    #        WYLD  Q QDR RESQ PET  ET  SW      erosion:txt[x]      QN  YN QDRN RSFN   QRFN  QP  YP QRFP QDRP STMP
    txt1 = ' 117  13  17  65  10  11 120' + txt[parm.txt_drv] + '  38  37  47  80' + '  84  49  48 142 143  59'
    lnum = 1
    tt = '   1'
    t1=''

    for txtline in parm.fnam1:
        if lnum == 8:  #Output variables needed for calibration
            txtline = txt1 + '\n' 
        elif lnum == 12:  
            if fsad==1:   #Enable *.SAD file
                t1 = txtline[0:40] + tt
            else:
                t1 = txtline[0:44]
             
            t1 = t1 + txtline[44:60]

            if fdws==1:    #Enable *.DWS file
                t1 = t1 + tt 
            else:
                t1 = t1 + txtline[60:64]

            t1 = t1 + txtline[64:len(txtline)]
            txtline = t1 
            
        elif lnum == 13:  
            t1 = txtline[0:12]
            if facy==1:  #Enable *.ACY file
                t1 = t1 + tt 
            else:
                t1 = t1 + txtline[12:16]

            t1 = t1 + txtline[16:56]

            if frch==1:   #Enable *.RCH file
                t1 = t1 + tt
            else:
                t1 = t1 + txtline[56:60]

            t1 = t1 + txtline[60:len(txtline)]
            txtline = t1 
        
        parm.fnam2.writelines(txtline) 
        lnum += 1
            
    parm.fnam1.close()
    parm.fnam2.close()
    os.remove(fnam)
    os.rename(parm.path_TxtWork + 'temp.txt',fnam)
