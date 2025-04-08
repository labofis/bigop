import os
import subprocess
import numpy as np
import xarray as xr
from mohid_ops import mohid_templates
import time

###############################################################################
# Download boundary conditions from CMEMS
###############################################################################
def download_cmems(start_date, end_date, storage_dir, variable):
    product_id = ('cmems_mod_glo_phy-' + variable + '_anfc_0.083deg_PT6H-i'
                  if variable != 'zos' else 'cmems_mod_glo_phy_anfc_0.083deg_PT1H-m')
    variable_name = variable if variable != 'cur' else 'uo -v vo'
    
    comando = (
        f'copernicusmarine subset -i {product_id} --username epassos --password 6Tilxl:Q0 '
        f'-v {variable_name} -t "{start_date}T00:00:00" -T "{end_date}T23:00:00" '
        f'-x -45.5 -X -43 -y -24.2 -Y -22.7 -z 0. -Z 156 -o {storage_dir} '
        f'-f cmems_{variable}_{start_date}.nc --force-download --disable-progress-bar --overwrite-output-data'
    )
    subprocess.run(comando, shell=True, check=True)

###############################################################################
# Wait for file creation
###############################################################################
def wait_for_file(file_path, timeout=300):
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Arquivo {file_path} não encontrado dentro do tempo limite!")
        time.sleep(5)

###############################################################################
# Join the boundary conditions from CMEMS
###############################################################################
def join_files(fileDir):
    arquivos = [x for x in os.listdir(fileDir) if x.endswith('.nc')]
    dataset = None
    for arquivo in arquivos:
        ds = xr.open_dataset(os.path.join(fileDir, arquivo))
        if dataset is None:
            dataset = ds
        else:
            dataset = xr.merge([dataset, ds])
    nome = f'cmems_{arquivos[0].split("_")[2]}'
    dataset.to_netcdf(os.path.join(fileDir, nome))
    dataset.close()
    print(' ')
    print('The CMEMS file with the merged variables is ready')
    print(' ')

###############################################################################
# Convert NetCDF files to HDF5 format
###############################################################################
def convert_cmems2hdf5(BASE_DIR, start_date, storage_dir, boundary_dir):
    action_file = mohid_templates.template_convert_action(start_date, storage_dir, boundary_dir)
    np.savetxt(os.path.join(BASE_DIR, 'ConvertToHDF5', 'ConvertToHDF5Action.dat'),
               np.array(action_file).reshape(1,), fmt='%s')

    os.chdir(os.path.join(BASE_DIR, 'ConvertToHDF5'))
    subprocess.run([os.path.join(BASE_DIR, 'ConvertToHDF5', 'Convert2Hdf5.exe')], check=True)
    os.chdir(BASE_DIR)

###############################################################################
# Configure simulation
###############################################################################
def config_sim(start_date, end_date, today_date):
    model_file = mohid_templates.template_model(start_date, end_date)
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
    exe_dir = os.path.join(BASE_DIR, 'mohid', 'exe')
    subprocess.run([os.path.join(exe_dir, 'MOHID_run.bat')], cwd=exe_dir, check=True)

# def run_mohid_sim(BASE_DIR):
#     exe_dir = os.path.join(BASE_DIR, 'mohid\exe')
#     subprocess.Popen(os.path.join(exe_dir,'MOHID_run.bat'),cwd=exe_dir)
#     time.sleep(300)