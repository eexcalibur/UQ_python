

from smt.sampling_methods import LHS
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from loguru import logger
import multiprocessing as mp

para_limits = np.array([
    [2.95e-3, 8.85e-3],
]
)

num = 100

base_path="/home/tzhang/scam_causal/SCAM_cesm/cesm1_2_2/SCMtest/run/"
archive_path = "/S2/gscr2/tzhang/big_data/UQ/scam_sampling/"
para_names = ['zmconv_c0_lnd']

sampling = LHS(xlimits=para_limits)
x = sampling(num)
print(x.shape)
print(x[0,:])

para_samples = []
for id, xx in enumerate(x):
    samp = {}
    for i,name in enumerate(para_names):
        samp[name] = xx[i]
    para_samples.append((id,samp))
    

def run_case(id,x):
    #create a case
    #print("cp -r "+base_path+"/runwrf "+base_path+"/case"+str(id))
    #os.system("cp -r "+base_path+"/runwrf "+base_path+"/case"+str(id))
    os.chdir(base_path)
    logger.info("case"+str(id)+": create a case")
    
    # modify namelist
    for key in x:
        replace_str = "sed -i '/^ "+key+"/c\ "+key+"="+str(x[key])+"' atm_in"
        os.system(replace_str)
    
    # run model
    #time.sleep(30)
    os.system("./scam >& /dev/null")
        
    #archive case
    archive_case = archive_path+"/case"+str(id)
    os.system("mkdir -p "+archive_case)
    os.system("cp atm_in "+archive_case)
    os.system("cp camrun.cam.h1.1995-07-19-00000.nc "+archive_case)
    
    
def run_case_wrapper(args):
    return run_case(*args)

pool = mp.Pool(1)
pool.map(run_case_wrapper,para_samples)
