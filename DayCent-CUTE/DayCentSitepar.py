import os, parm
import msgbox

def update():
    # This module updates sitepar.in file with new demflux and dem values    
    fnam = parm.path_TxtWork + '/' + parm.fnam_sitepar    # sitepar.in
    try:
        parm.fnam1 = open(fnam, 'r+')
    except:
        #Print error message and exit
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    parm.fnam2 = open(parm.path_TxtWork + 'temp.tmp','w') #temp file

    linestr = parm.fnam1.readlines()  # sitepar.in

    # read parm values from sitepar.in  # This loop is not efficient, better to use python dictionary comprehension
    for i in range(0, 22):  # total lines 38
        txtline = linestr[i]
        dum = ' '.join(txtline.split())
        data = dum.split(' ')
        for j in range(0, len(parm.par_name)):
            if data[2] == parm.par_name[j].replace(" ",""):
                txt = str("{:8.6f}".format(parm.cur_test_var[j]))
                txt = txt + '   / ' + data[2] + '\n'
                linestr[i] = txt
                break

    # reprint sitepar.in
    parm.fnam2.writelines(linestr[0:len(linestr)])
            
    parm.fnam1.close()
    parm.fnam2.close()
    os.remove(fnam)
    os.rename(parm.path_TxtWork + 'temp.tmp',fnam)

    
    
 
 
