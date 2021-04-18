from netCDF4 import Dataset
import numpy as np

from netCDF4 import Dataset
def calc_metrics(path_mod):

    # define path and load data
    var_list = ['dir','dif'] # dni: direct normal irradiance DHI: diffuse horizontal irradiance
    varn_obs = ['obs_swddir', 'obs_swddif']
    varn_mod = ['SWDDIR','SWDDIF']

    path_base = "/ss/hsdc/home/tzhang/wrf_solar/"
    path_obs = path_base+"sgpradflux10long_area_mean.c1.20160619_1200UTC.nc"
    path_def = "/S2/gscr2/tzhang/big_data/UQ/tune/runwrf_def/wrfout_d02_2016-06-19_06:00:00"

    fid_obs = Dataset(path_obs)
    fid_def = Dataset(path_def)
    fid_mod = Dataset(path_mod)

    data_obs = {}
    data_def = {}
    data_mod = {}

    for i,varn in enumerate(var_list):
        data_obs[varn] = fid_obs.variables[varn_obs[i]][:]
        data_mod[varn] = np.mean(fid_mod.variables[varn_mod[i]][36:],axis=(1,2))
        data_def[varn] = np.mean(fid_def.variables[varn_mod[i]][36:],axis=(1,2))

    data_obs['tot'] = data_obs['dir'] + data_obs['dif']
    data_mod['tot'] = data_mod['dir'] + data_mod['dif']
    data_def['tot'] = data_def['dir'] + data_def['dif']


    # compute metrics
    metrics_list = ['tot','dir']

    Chi = 0
    for var in metrics_list:
        theta_mod = 0
        for j in range(data_obs[var].shape[0]):
            theta_mod += (data_obs[var][j] - data_mod[var][j]) ** 2

        theta_def = 0
        for j in range(data_obs[var].shape[0]):
            theta_def += (data_obs[var][j] - data_def[var][j]) ** 2

        Chi += (theta_mod / theta_def)

    Chi /= len(var_list)

    return Chi
        
if __name__ == '__main__':
    aa = calc_metrics("/S2/gscr2/tzhang/big_data/UQ/tune/runwrf_def/wrfout_d02_2016-06-19_06:00:00")
    print(aa)
