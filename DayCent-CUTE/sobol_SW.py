import numpy as np
#from scipy.stats import norm  # could not find a working scipy library, so cannot calculate confidence intervals now, which is fine if the sample size is big enough.
from SALib.util import read_param_file
import parm

# Perform Sobol Analysis on file of model results

DAT=[]
def analyze(pfile, output_file, delim = ' ', calc_second_order = True, num_resamples = 1000,
             print_to_console=False):
    
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
    if calc_second_order and Y.size % (2*D + 2) == 0:
        N = int(Y.size / (2*D + 2))
    elif not calc_second_order and Y.size % (D + 2) == 0:
        N = int(Y.size / (D + 2))
    else: raise RuntimeError("""
         Incorrect number of samples in model output file. 
         Confirm that calc_second_order matches option used during sampling.""")  
           
    A = np.empty(N)
    B = np.empty(N)
    AB = np.empty((N,D))
    BA = np.empty((N,D)) if calc_second_order else None
    step = 2*D+2 if calc_second_order else D+2

    # First order (+conf.) and Total order (+conf.)
    #keys = ('S1','S1_conf','ST','ST_conf')
    keys = ('S1','ST')
    S = dict((k, np.empty(D)) for k in keys)
  
    #z=0
    for ii in range(0,n):    
       #if z == 0 or z == n-1: # using average annual output and the last year output
           #Y = np.loadtxt(output_file, delimiter=',', usecols=(z,))    
           Y = np.loadtxt(output_file, delimiter=',', usecols=(ii,))    
           A = Y[0:Y.size:step]
           B =  Y[(step-1):Y.size:step]
           for j in range(D):
              AB[:,j] = Y[(j+1):Y.size:step]
              if calc_second_order: BA[:,j] = Y[(j+1+D):Y.size:step]         
          #for j in range(D):
              S['S1'][j] = first_order(A, AB[:,j], B)
              #S['S1_conf'][j] = first_order_confidence(A, AB[:,j], B, num_resamples, conf_level)
              S['ST'][j] = total_order(A, AB[:,j], B)
              #S['ST_conf'][j] = total_order_confidence(A, AB[:,j], B, num_resamples, conf_level)
        
            # Second order
           if calc_second_order:
              S['S2'] = np.empty((D,D)); S['S2'][:] = np.nan
              #S['S2_conf'] = np.empty((D,D)); S['S2_conf'][:] = np.nan
                
           for j in range(D):
              for k in range(j+1, D):     
                  S['S2'][j,k] = second_order(A, AB[:,j], AB[:,k], BA[:,j], B)
                  #S['S2_conf'][j,k] = second_order_confidence(A, AB[:,j], AB[:,k], BA[:,j], B, num_resamples, conf_level)

           p_string1 = ["%8.3f" % x for x in S['S1']]
           p_string2 = ["%8.3f" % x for x in S['ST']]      
           #p_string3 = ["%.3f" % x for x in S['S2']] # this cannot be converted, so for now teh Second_Order indices are not outputed.           
           #p_string1 = np.hstack((C1[z], p_string1))  
           p_string1 = np.hstack((C1[ii], p_string1))  
           p_string2 = np.hstack((C2[ii], p_string2))  

           #if z>0:             
           if ii>0:             
               DAT = np.column_stack((DAT,p_string2,p_string1))
           else:               
               DAT = np.column_stack((nam,p_string2,p_string1))
      # z += 1
    np.savetxt('sobolIndices.csv', DAT, fmt='%s',delimiter=',')                      
        
def first_order(A, AB, B):
    # First order estimator following Saltelli et al. 2010 CPC, normalized by sample variance
    return np.mean(B*(AB-A))/np.var(np.r_[A,B])

def first_order_confidence(A, AB, B, num_resamples, conf_level):
    s  = np.empty(num_resamples)
    for i in range(num_resamples):        
        r = np.random.randint(len(A), size=len(A))        
        s[i] = first_order(A[r], AB[r], B[r])
    
    return norm.ppf(0.5 + conf_level/2) * s.std(ddof=1)

def total_order(A, AB, B):
    # Total order estimator following Saltelli et al. 2010 CPC, normalized by sample variance
    return 0.5*np.mean((A-AB)**2)/np.var(np.r_[A,B])

def total_order_confidence(A, AB, B, num_resamples, conf_level):
    s  = np.empty(num_resamples)    
    for i in range(num_resamples):
        r = np.random.randint(len(A), size=len(A))  
        s[i] = total_order(A[r], AB[r], B[r])
    
    return norm.ppf(0.5 + conf_level/2) * s.std(ddof=1)

def second_order(A, ABj, ABk, BAj, B):
    # Second order estimator following Saltelli 2002
    V = np.var(np.r_[A,B])
    Vjk = np.mean(BAj*ABk - A*B)
    Sj = first_order(A,ABj,B)
    Sk = first_order(A,ABk,B)
    
    return Vjk/V - Sj - Sk

def second_order_confidence(A, ABj, ABk, BAj, B, num_resamples, conf_level):
    s  = np.empty(num_resamples)
    for i in range(num_resamples):
        r = np.random.randint(len(A), size=len(A))
        s[i] = second_order(A[r], ABj[r], ABk[r], BAj[r], B[r])
    
    return norm.ppf(0.5 + conf_level/2) * s.std(ddof=1)
