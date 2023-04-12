import os, parm
import numpy as np
import msgbox

def update():
    #This module updates DayCent's FIX.100 file with new set of parameters
    fnam = parm.path_TxtWork + '/' + parm.fnam_parm      # FIX.100
    try:
        parm.fnam1 = open(fnam, 'r+')
    except:
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return
   
    # Create a temporary file
    try:
         parm.fnam2 = open(parm.path_TxtWork + '/' +'temp.tmp','w') #temp file
    except:
        parm.error_msg = "An error was occurred while \n creating temp.tmp for DayCent FIX.100 file."
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    linestr= parm.fnam1.readlines()     #  FIX.100

    # read parm values from fix.100  # the first 169 lines in the FIX.100 which includes listed parms in plist
    # This loop is not efficient, better to use python dictionary comprehension
    n=0
    for i in range (1,170):   # total lines 225
        txtline = linestr[i]
        dum = ' '.join(txtline.split())
        data = dum.split(' ')
        for j in range (n, len(parm.par_name)):
            #if data[1].replace("'", "") == parm.par_name[j].replace("_", ",") or data[1].replace("'", "") == 'PRDX_G3N(1)':
            if data[1].replace("'", "") == parm.par_name[j].replace("_", ","):                
                txt = str("{:8.5f}".format(parm.cur_test_var[j]))
                txt = txt +'      ' + data[1] + '\n'
                linestr[i] = txt
                n +=1
                break
        if n == len(parm.par_name): break

    # reprint FIX.100
    parm.fnam2.writelines(linestr[0:len(linestr)]) 
    
    parm.fnam1.close()
    parm.fnam2.close()
    os.remove(fnam)
    os.rename(parm.path_TxtWork + '\\temp.tmp',fnam)

#def chunkstring(string, length):
#    return (string[0+ii:length+ii] for ii in range(0, len(string), length))




