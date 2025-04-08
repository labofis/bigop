"""
Run daily operational simulation with MOHID Water Modeling System
Autor: Douglas Fraga Rodrigues
Alterado por Elisa Passos
"""

import os
import subprocess
import datetime
from pathlib import Path
from mohid_ops import mohid_preprocessing

###############################################################################
# Define working folder
###############################################################################
BASE_DIR = Path(__file__).resolve().parent

storage_dir = os.path.join(BASE_DIR, 'nc')
boundary_dir = os.path.join(BASE_DIR, 'bc_hdf5')

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
# os.chdir(storage_dir)
# # Remove previous files
# for arq in os.listdir():
#     if arq.endswith('.nc'):
#         os.remove(arq)

# # Download new boundary conditions
# variables = ['thetao', 'so', 'cur', 'zos']
# for var in variables:
#     mohid_preprocessing.download_cmems(start_date, end_date, storage_dir, var)
#     mohid_preprocessing.wait_for_file(os.path.join(storage_dir, f'cmems_{var}_{start_date}.nc'))

# # Join the downloaded files into a single NetCDF file
# mohid_preprocessing.join_files(storage_dir)

###############################################################################
# Convert NetCDF files to HDF5 format
###############################################################################
# mohid_preprocessing.convert_cmems2hdf5(BASE_DIR, start_date, storage_dir, boundary_dir)

###############################################################################
# Update MOHID configuration files
###############################################################################
# mohid_preprocessing.config_sim(start_date, end_date, today_date)

###############################################################################
# Run MOHID simulation
###############################################################################
mohid_preprocessing.run_mohid_sim(BASE_DIR)

print(u'Execução bem sucedida!')
