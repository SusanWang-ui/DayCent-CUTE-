import os, parm
import msgbox

def update():
    # This module updates <site>.100 file for FBM and FHP    
    fnam = parm.path_TxtWork + '\\' + parm.site_fn       # site file name is listed in line 3 in .sch file
    try:
        parm.fnam1 = open(fnam, 'r+')
    except:
        #Print error message and exit
        parm.error_msg = fnam + ' is not found.'
        msgbox.msg("Error", parm.error_msg)
        parm.iflg=1; return

    parm.fnam2 = open(parm.path_TxtWork + 'temp.tmp','w') #temp file

    linestr = parm.fnam1.readlines()  # <site>.100

    # read parm values from <site>.100
    k=0
    for i in range(0, 200):  # total lines >200
        txtline = linestr[i]
        dum = ' '.join(txtline.split())
        data = dum.split(' ')
        if data[1] == 'IVAUTO': 
            linestr[i] = '0.0               ' + data[1] + '\n'
        elif data[1] == 'SOM1CI(2,1)': 
            soc_val1 = float(data[0]) 
            txtline = linestr[i+4]
            dum = ' '.join(txtline.split())
            data = dum.split(' ')
            soc_val2 = float(data[0])
            txtline = linestr[i+6]
            dum = ' '.join(txtline.split())
            data = dum.split(' ')
            soc_val3 = float(data[0])
            soc_val = soc_val1 + soc_val2 + soc_val3
            k=i
            break

    for j in range(0, len(parm.par_name)):
        if parm.par_name[j]=='FBM':
            soc_val1 = soc_val*parm.cur_test_var[j]            
        elif parm.par_name[j]=='FHP':
            soc_val3 = parm.cur_test_var[j]*(soc_val-soc_val1)
            soc_val2 = soc_val - soc_val1 - soc_val3
            break

    linestr[k] = str("{:9.4f}".format(soc_val1) + '         SOM1CI(2,1)' + '\n')
    kk=k+4
    linestr[kk] = str("{:9.4f}".format(soc_val2) + '         SOM2CI(2,1)' + '\n')
    kk=k+6
    linestr[kk] = str("{:9.4f}".format(soc_val3) + '         SOM3CI(1)' + '\n')
    # reprint <site>.100
    parm.fnam2.writelines(linestr[0:len(linestr)])
            
    parm.fnam1.close()
    parm.fnam2.close()
    os.remove(fnam)
    os.rename(parm.path_TxtWork + 'temp.tmp',fnam)
