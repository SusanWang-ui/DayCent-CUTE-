import os, parm
import numpy as np
import msgbox

def update():
    #This module updates DayCent's CULT.100 file for CULT A-K with a given "Till_Eff" 
    fnam = parm.path_TxtWork + '\\cult.100'      # CULT.100
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

    for j in range(0, len(parm.par_name)):
        if parm.par_name[j].upper()=='TILL_EFF':
            culteffK_value = parm.cur_test_var[j]        
            break

    cult100 = parm.fnam1.readlines()     #  read CULT.100
    tillages = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    till_adjust = [0.0144, 0.1156, 0.1878, 0.2678, 0.3167, 0.3911, 0.4733, 0.5622, 0.6300, 0.9711, 1.0]
    index=0
    for i in range(len(tillages)):
        for pos in range(index, len(cult100)):
            if tillages[i] == cult100[pos][0]:
                culteff = round(1 + (culteffK_value -1)*till_adjust[i], 4)
                cult100[pos + 8]  = str("{:6.4f}".format(culteff))+"            'CLTEFF(1)'"+'\n'
                cult100[pos + 9]  = str("{:6.4f}".format(culteff))+"            'CLTEFF(2)'"+'\n'
                cult100[pos + 11] = str("{:6.4f}".format(culteff))+"            'CLTEFF(4)'"+'\n'
                index = pos + 11
                break

    # reprint CULT.100
    parm.fnam2.writelines(cult100) 
    
    parm.fnam1.close()
    parm.fnam2.close()
    os.remove(fnam)
    os.rename(parm.path_TxtWork + '\\temp.tmp',fnam)

#def chunkstring(string, length):
#    return (string[0+ii:length+ii] for ii in range(0, len(string), length))




