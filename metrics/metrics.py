from netCDF4 import Dataset
import numpy as np

def calc_metrics(path_mod):
    var_list = ['dni','dhi'] # dni: direct normal irradiance DHI: diffuse horizontal irradiance
    varn_obs = ['obs_swddni', 'obs_swddif']
    varn_mod = ['SWDDNI','SWDDIF']
    
    path_base = "/ss/hsdc/home/tzhang/wrf_solar/"
    path_obs = path_base+"sgpradflux10long_area_mean.c1.20160619_1200UTC.nc"
    path_def = "/S2/gscr2/tzhang/big_data/UQ/tune/runwrf_def/wrfout_d02_2016-06-19_06:00:00"
    
    fid_obs = Dataset(path_obs)
    fid_def = Dataset(path_def)
    fid_mod = Dataset(path_mod)
    
    Chi = 0
    for i, var in enumerate(var_list):
        #print(var)
        
        var_obs = fid_obs.variables[varn_obs[i]][:]
        var_mod = fid_mod.variables[varn_mod[i]][36:]
        var_def = fid_def.variables[varn_mod[i]][36:]
        
        var_mod_avg = np.mean(var_mod, axis=(1,2))
        var_def_avg = np.mean(var_def, axis=(1,2))
        
        #print(var_obs.shape)
        #print(var_mod_avg.shape)
        #print(var_def_avg.shape)
        
        theta_mod = 0
        for j in range(var_obs.shape[0]):
            theta_mod += (var_obs[j] - var_mod_avg[j]) ** 2
            
        theta_def = 0
        for j in range(var_obs.shape[0]):
            theta_def += (var_obs[j] - var_def_avg[j]) ** 2
            
        Chi += (theta_mod / theta_def)
        
    Chi /= len(var_list)
    
    return Chi
            
        
if __name__ == '__main__':
    calc_metrics("/S2/gscr2/tzhang/big_data/UQ/tune/runwrf_def/wrfout_d02_2016-06-19_06:00:00")
