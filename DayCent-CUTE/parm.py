# DayCent-CUTE Version
cute_rev=''

txt=''
fnam1=''
fnam2=''
val=1000000

reset_config_status=0

#files
proj_cur=0
file_proj=''
file_ddsout=''
cute_path=''
path_proj=''
path_DayCent=''
path_TxtInout=''
path_TxtWork=''
path_obs=''
obs_dt=[]
dds_stat=''
of_weight=[]
DayCent_var=[]
DayCent_outputFile=[]
DayCent_crop=[]

dds_pertsize=0.2
dds_ndraw=1000
dds_useinit=1
dds_restart=0
dds_icall=0
dds_prerun = 0

#Total DayCent parameters to evaluate.
par_ID=[]
par_name=[]
par_initval=[]
par_bl=[]
par_bu=[]
par_cropname=[]
par_filename=[]

#parameters in DayCent FIX100 table
DayCent_par_name=[]
DayCent_par_initval=[]
DayCent_par_bl=[]
DayCent_par_bu=[]
DayCent_par_filename=[]

#parameters in PARMS table
PARMS_par_name=[]
PARMS_par_initval=[]
PARMS_par_bl=[]
PARMS_par_bu=[]

#parameters in Crop Parameters table
CROP_par_name=[]
CROP_par_initval=[]
CROP_par_bl=[]
CROP_par_bu=[]
CROP_par_cropname=[]


#Constraints in the constraints.csv
cs1=0 #baseflow or pet, 0=constraints off, 1=on
cs100=0 #crop yield, 0=constraints off, 1=on
cs_on=0 #0=do not use constraints, 1=use
cs_type=[]
cs_name=[]
cs_bl=[]
cs_bu=[]
baseflow_ratio=0
pet=0
crop_yld=[]
obs_yld_type=''

cur_best_var=[]
cur_best_OF=1000
cur_test_var=[]
cur_test_OF=0
pre_best_OF = 0

SCHFile=None
txt_beginYr=1900       # Beginning year of simulation, example only
txt_endYr=2000         # Last year of simulation, example only
txt_imo=1
txt_ida=1
txt_ipd=6
txt_nvcn=4
txt_infl=0
txt_outputSYr=1992   # Output starting year, example only

fnam_outvars=''   # not used now, but will be used to rewrite outvars.txt based on user selected output/s
fnam_sitepar='sitepar.in'
fnam_lis=''
fnam_parm='FIX.100'
fnam_opc=''  #
fnam_sol=''  #
Site_name=''   # Name or study name for DayCent run
site_fn=''     # site file name
fnam_crop=''
fnam_obs=''

# Variables indicating if to update DayCent FIX.100, sitepar.in, cult.100, and/or crop.100 files
iparm=0
isite100=0
isitepar=0
icrop100=0
cult100=0

# Input/output files
ISCH=''   # .sch file name only
IBIN=''   # .bin of previous simulation file (file name only) to initialize the model
IOPS=0 #.opc/s file ID from operation schedule list (OPSCCOM.dat).
ISOL=0 #.sol file ID from soil list (SOILCOM.DAT).

pred_day_count=[]
pred_date=[]
pred_datea=[] 
pred_val=[]
pred_vala=[]

obs_date=[]
obs_val = []
pairdCal=[]
pairdVal=[]
pairpCal=[]
pairoCal=[]
pairpVal=[]
pairoVal=[]

start_pred=[]    #
start_obs=[]
start_cal=0
end_pred=[]
end_obs=[]
end_cal=0
start_val=0
end_val=0

bias=0  # ABSOLUTE ERROR
bias1=0 # (pred-obs)/n
meanpr=0
stdpr=0
rmse=0
r2=0
re=0
nse=0

pred_fSA=[]   # saves selected APEX output (avg and yearly values) 
# used in SA component
pred_fSAm=[]  # saves average annual results for selected outputs
SA_method=1   # used in SA component; Sobol=1,FAST=2.
NumPar_fSA=0  # number of parameters considered in SA.
SA_orCal=0  # default 0 is for calibration; 1 is for sensitivity analysis; 2 for DayCent run only (single or batch run)
SA_n=0    # SA initial sample size.

flg_path_save=0
flg_option_save=0
flg_constraints_save=0
flg_crop_save=0
flg_parms_save=0
flg_DayCentparameters_save=0
flg_validation=0
flg_cute_setting_save=0
iflg=0    # 0: no log Error message
cute_option = ''

sa_n_iter=1

#parameter type in the PARM file
#water=1; sediment=2, N=3, P=4, C=5, pesticide=6, crop=7, Not used=0
parm_type=[]
parm_type[1:10]=[1,7,7,3,1,7,3,4,6,6]
parm_type[11:20]=[7,1,2,3,1,1,1,2,2,1]
parm_type[21:30]=[5,1,1,6,1,7,3,3,3,7]
parm_type[31:40]=[3,4,2,1,0,3,2,7,1,1]
parm_type[41:50]=[7,1,5,1,2,5,5,7,1,1]
parm_type[51:60]=[1,3,7,3,3,7,4,4,4,7]
parm_type[61:70]=[1,2,3,2,2,2,2,2,2,2]
parm_type[71:80]=[2,3,1,3,4,7,6,7,7,3]
parm_type[81:90]=[7,0,1,4,4,3,1,1,1,1]
parm_type[91:100]=[1,1,2,2,5,4,7,0,0,5]
parm_type[101:110]=[5,3,3,3,3,3,3,3,3,3]

si_parm=[]
si_first=[]
si_total=[]
dds_head=[]
dds_data=[]
error_msg=''

