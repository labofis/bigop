"""
Run daily operational simumation with MOHID Water Modeling System
Autor: Douglas Fraga Rodrigues
"""
import os
import time
import datetime
from pathlib import Path
from mohid_ops import mohid_preprocessing

###############################################################################
# Define working folder
###############################################################################
BASE_DIR = Path(__file__).resolve().parent
print('BASE: ',BASE_DIR)

storage_dir = os.path.join(BASE_DIR / 'nc')
boundary_dir = os.path.join(BASE_DIR / 'bc_hdf5')

###############################################################################
# Define simulation dates
###############################################################################
today = datetime.datetime.today()
start_date = today.strftime('%Y-%m-%d')
today_date = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
end_date = (today + datetime.timedelta(days=2)).strftime('%Y-%m-%d')

###############################################################################
# Download boundary conditions from CMEMS
###############################################################################
# # os.chdir(storage_dir)
[os.remove(arq) for arq in os.listdir() if arq.endswith('.nc')]

# mohid_preprocessing.download_cmems(start_date,end_date,storage_dir,'thetao')
# mohid_preprocessing.download_cmems(start_date,end_date,storage_dir,'so')
# mohid_preprocessing.download_cmems(start_date,end_date,storage_dir,'cur')
# mohid_preprocessing.download_cmems(start_date,end_date,storage_dir,'zos')

# mohid_preprocessing.join_files(storage_dir)
# time.sleep(300)

###############################################################################
# Convert NetCDF files to HDF5 format
###############################################################################
# mohid_preprocessing.convert_cmems2hdf5(BASE_DIR,start_date,storage_dir,boundary_dir)
# time.sleep(60)

###############################################################################
# Update MOHID configuration files
###############################################################################
# mohid_preprocessing.config_sim(start_date,end_date,today_date)
# time.sleep(60)

###############################################################################
# Run MOHID simulation
###############################################################################
# mohid_preprocessing.run_mohid_sim(BASE_DIR)


###############################################################################
# Create surface current maps
###############################################################################
# mohid_postprocessing.surface_current_map(BASE_DIR,today_date)


print(u'Execução bem sucedida!')
