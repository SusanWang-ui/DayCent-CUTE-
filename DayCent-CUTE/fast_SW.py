from SALib.util import read_param_file
from sys import exit
import numpy as np
import math, parm

# Perform FAST Analysis on file of model results
# Returns a dictionary with keys 'S1' and 'ST'
# Where each entry is a list of size D (the number of parameters)
# Containing the indices in the same order as the parameter file
DAT=[]
def analyze(pfile, output_file, column = 0, M = 4, delim = ' ', print_to_console=False):
    
    param_file = read_param_file(pfile)
    D = param_file['num_vars']
    nam1 = 'Pname'
    nam=np.array(param_file['names'])   
    nam=np.hstack((nam1,nam))

    n = len(parm.DayCent_var)
    C1=np.empty(n,dtype="S14")
    C2=np.empty(n,dtype="S14")
    for k in range(n):        
        C1[k] = 'F_' + parm.DayCent_var[k]
        C2[k] = 'T_' + parm.DayCent_var[k]

    Y=np.loadtxt(output_file, delimiter=',',usecols=(0,))    
    #np.savetxt('Ylytest.csv', Y, fmt='%s',delimiter=',')  #debug to check if read right.
    
    if Y.size % (D) == 0:
        N = int(Y.size / D)
    else:
 #       print """
 #           Error: Number of samples in model output file must be a multiple of D,
 #           where D is the number of parameters in your parameter file.
 #         """
        exit()

    # Recreate the vector omega used in the sampling
    omega = np.empty([D])
    omega[0] = math.floor((N - 1) / (2 * M))
    m = math.floor(omega[0] / (2 * M))
    
    if m >= (D-1):
        omega[1:] = np.floor(np.linspace(1, m, D-1)) 
    else:
        omega[1:] = np.arange(D-1) % m + 1

    # Calculate and Output the First and Total Order Values
    Si = dict((k, [None]*D) for k in ['S1','ST'])
    #z=0
    for ii in range(0,n):  
        Y=np.loadtxt(output_file, delimiter=',',usecols=(ii,))
        for i in range(D):
            l = range(i*N, (i+1)*N)
            Si['S1'][i] = compute_first_order(Y[l], N, M, omega[0])
            Si['ST'][i] = compute_total_order(Y[l], N, omega[0]) 
                          
        p_string1 = ["%9.3f" % x for x in Si['S1']]   
        p_string2 = ["%9.3f" % x for x in Si['ST']]           
        p_string1 = np.hstack((C1[ii], p_string1))  
        p_string2 = np.hstack((C2[ii], p_string2))        

        if ii>0:           
            DAT = np.column_stack((DAT,p_string2,p_string1))
        else:
             DAT = np.column_stack((nam,p_string2,p_string1))
    np.savetxt('fastIndices.csv', DAT, fmt='%s',delimiter=',') 
        
def compute_first_order(outputs, N, M, omega):
    f = np.fft.fft(outputs)
    Sp = np.power(np.absolute(f[range(1,int(N/2))]) / N, 2)
    V = 2*np.sum(Sp)
    D1 = 2*np.sum(Sp[list(np.arange(1,M+1)*int(omega) - 1)])
    return D1/V

def compute_total_order(outputs, N, omega):
    f = np.fft.fft(outputs)
    Sp = np.power(np.absolute(f[range(1,int(N/2))]) / N, 2)
    V = 2*np.sum(Sp)
    Dt = 2*sum(Sp[range(int(omega/2))])
    return (1 - Dt/V)
