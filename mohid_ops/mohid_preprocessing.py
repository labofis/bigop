"""
Run daily operational simumation with MHID Water Modeling System
Autor: Douglas Fraga Rodrigues
Alterado por Elisa Passos
"""
import os
import time
import subprocess
import subprocess, sys
import numpy as np
import xarray as xr
from mohid_ops import mohid_templates


###############################################################################
# Download boundary conditions from CMEMS
###############################################################################
def download_cmems(start_date,end_date,storage_dir,variable):
    product_id = ['cmems_mod_glo_phy-'+variable+'_anfc_0.083deg_PT6H-i' if variable != 'zos' else 'cmems_mod_glo_phy_anfc_0.083deg_PT1H-m'][0]
    variable_name = [variable if variable != 'cur' else 'uo -v vo'][0]
    
    comando = 'copernicusmarine subset -i '+product_id+' --username epassos --password 6Tilxl:Q0 -v '+variable_name+' -t "'+start_date+'T00:00:00" -T "'+end_date+'T23:00:00" -x -45.5 -X -43 -y -24.2 -Y -22.7 -z 0. -Z 156 -o '+storage_dir+' -f cmems_'+variable+'_'+start_date+'.nc --disable-progress-bar'
    os.system(comando)
    

###############################################################################
# Join the boundary conditions from CMEMS
###############################################################################
def join_files(fileDir):

    arquivos = [x for x in os.listdir(fileDir) if x.endswith('.nc')]
    dataset = xr.Dataset()
    for arquivo in arquivos:
        variable = arquivo.split('_')[1]
        ds =  xr.open_dataset(os.path.join(fileDir,arquivo))
        if variable != 'cur':
            dataset[variable] = ds[variable]
        else:
            dataset['uo'] = ds.uo
            dataset['vo'] = ds.vo
        ds.close()
    nome = 'cmems_'+arquivo.split('_')[2]
    dataset.to_netcdf(os.path.join(fileDir,nome))
    dataset.close()
    
    # time.sleep(60)
    
    # ds = xr.open_dataset(os.path.join(fileDir,nome))
    # ds.close()
    # [os.remove(os.path.join(fileDir,arq)) for arq in arquivos]
    
###############################################################################
# Convert NetCDF files to HDF5 format
###############################################################################
def convert_cmems2hdf5(BASE_DIR,start_date,storage_dir,boundary_dir):
    action_file = mohid_templates.template_convert_action(start_date,storage_dir,boundary_dir)
    np.savetxt('ConvertToHDF5/ConvertToHDF5Action.dat', np.array(action_file).reshape(1,), fmt='%s')

    os.chdir(os.path.join(BASE_DIR, 'ConvertToHDF5'))
    os.system(os.path.join(BASE_DIR, 'ConvertToHDF5','Convert2Hdf5.exe'))
    os.chdir(BASE_DIR)

    # time.sleep(60)

###############################################################################
# Configure simulation
###############################################################################
def config_sim(start_date,end_date,today_date):
    model_file = mohid_templates.template_model(start_date,end_date)
    np.savetxt('mohid/data/Model_1.dat', np.array(model_file).reshape(1,), fmt='%s')
    np.savetxt('mohid/L01/data/Model_1.dat', np.array(model_file).reshape(1,), fmt='%s')

    nomfich_file = mohid_templates.template_nomfich(today_date)
    np.savetxt('mohid/L01/exe/Nomfich.dat', np.array(nomfich_file).reshape(1,), fmt='%s')

    assimilation_file = mohid_templates.template_assimilation(start_date)
    np.savetxt('mohid/L01/data/Assimilation_1.dat', np.array(assimilation_file).reshape(1,), fmt='%s')

    waterproperties_file = mohid_templates.template_waterproperties(start_date)
    np.savetxt('mohid/L01/data/WaterProperties_1.dat', np.array(waterproperties_file).reshape(1,), fmt='%s')


###############################################################################
# Run simulation
###############################################################################
def run_mohid_sim(BASE_DIR):
    # time.sleep(300)
    exe_dir = os.path.join(BASE_DIR, 'mohid\exe')
    subprocess.Popen(os.path.join(exe_dir,'MOHID_run.bat'),cwd=exe_dir)
