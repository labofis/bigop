"""
Configuration templates for MOHID simulations
Autor: Douglas Fraga Rodrigues
"""


def template_convert_action(start_date,storage_dir,boundary_dir):
    return f"""
<begin_file>
 
ACTION : CONVERT NETCDF CF TO HDF5 MOHID
HDF5_OUT : 1
NETCDF_OUT : 0
OUTPUT_NETCDF_FILE : NULL.nc
OUTPUTFILENAME           : {boundary_dir}\cmems_{start_date}.hdf5
 
<<begin_time>>
NETCDF_NAME : time
<<end_time>>
 
<<begin_grid>>
NETCDF_NAME_LAT : latitude
NETCDF_NAME_LONG : longitude
NETCDF_NAME_MAPPING : uo
MAPPING_LIMIT : -32000
INVERT_LAYER_ORDER : 1
NETCDF_NAME_DEPTH   : depth
BATHYM_FROM_MAP : 1
BATHYM_FILENAME : CMEMS_GridData.dat
<<end_grid>>
 
PROPERTIES_NUMBER : 6
 
<<begin_field>>
NETCDF_NAME : uo
NAME : velocity U
UNITS : m/s
DESCRIPTION : MOHID
DIM : 3
ADD_FACTOR      : 0.
MULTIPLY_FACTOR : 6.103701889514923E-4
!FILL_VALUE      : -99
<<end_field>>
 
<<begin_field>>
NETCDF_NAME : zos
NAME : water level
UNITS : m
DESCRIPTION : MOHID
DIM : 2
ADD_FACTOR      : 0.
MULTIPLY_FACTOR :  3.0518509447574615E-4
!FILL_VALUE      : -99
<<end_field>>
 
<<begin_field>>
NETCDF_NAME : thetao
NAME : temperature
UNITS : °C
DESCRIPTION : MOHID
DIM : 3
ADD_FACTOR      : 21.
MULTIPLY_FACTOR : 7.324442267417908E-4
!FILL_VALUE      : -99
<<end_field>>
 
<<begin_field>>
NETCDF_NAME : so
NAME : salinity
UNITS : psu
DESCRIPTION : MOHID
DIM : 3
ADD_FACTOR      : -0.0015259254723787308
MULTIPLY_FACTOR :  0.0015259254723787308
!FILL_VALUE      : -99
<<end_field>>
 
<<begin_field>>
NETCDF_NAME : vo
NAME : velocity V
UNITS : m/s
DESCRIPTION : MOHID
DIM : 3
ADD_FACTOR      : 0.
MULTIPLY_FACTOR :  6.103701889514923E-4
!FILL_VALUE      : -99
<<end_field>>
 
<<begin_field>>
NETCDF_NAME : velocity_modulus
NAME : velocity modulus
UNITS : m/s
DESCRIPTION : MOHID
DIM : 3
VECTOR_INTENSITY         : 1
VECTOR_X                 : velocity U
VECTOR_Y                 : velocity V
!FILL_VALUE      : -99
<<end_field>>
 
<<begin_input_files>>
{storage_dir}\cmems_{start_date}.nc
<<end_input_files>>
 
<end_file>
"""


def template_model(start_date,end_date):
    start_y = start_date[:4]; start_m = start_date[5:7]; start_d = start_date[8:]
    end_y = end_date[:4]; end_m = end_date[5:7]; end_d = end_date[8:]
    return f"""
START                     : {start_y} {start_m} {start_d} 12 0 0
END                       : {end_y} {end_m} {end_d} 0 0 0
DT                        : 60
VARIABLEDT                : 0
MAXDT                     : 3600
GMTREFERENCE              : -3
DT_PREDICTION_INTERVAL    : 60
"""


def template_assimilation(start_date):
    return f"""
<beginproperty>
NAME                    : water level
UNITS                   : m
DIMENSION               : 2D
OUTPUT_HDF              : 1
<<begin_field>>
DEFAULTVALUE            : 0
INITIALIZATION_METHOD   : HDF
FILE_IN_TIME            : HDF
FIELD4D                 : 1
SPATIAL_INTERPOL        : 1
EXTRAPOLATE             : 1
COLD_RELAX_PERIOD       : 43200.
COLD_ORDER              : 5
FILENAME                : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
TYPE_ZUV                : z
<<end_field>>
<<begin_coef>>
DEFAULTVALUE            : 1e5
TYPE_ZUV                : z
FILE_IN_TIME            : NONE
REMAIN_CONSTANT         : 1
INITIALIZATION_METHOD   : SPONGE
SPONGE_OUT              : 1e5
<<end_coef>>
<endproperty>
    
<beginproperty>
NAME                    : velocity U
UNITS                   : m/s
DIMENSION               : 3D
OUTPUT_HDF              : 1
COLD_RELAX_PERIOD       : 43200.
COLD_ORDER              : 5
<<begin_field>>
DEFAULTVALUE            : 0
INITIALIZATION_METHOD   : HDF
FILE_IN_TIME            : HDF
FIELD4D                 : 1
SPATIAL_INTERPOL        : 1
EXTRAPOLATE             : 1
FILENAME                : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
TYPE_ZUV                : z
<<end_field>>
<<begin_coef>>
DEFAULTVALUE            : 1e5
TYPE_ZUV                : u
FILE_IN_TIME            : NONE
REMAIN_CONSTANT         : 1
INITIALIZATION_METHOD   : SPONGE
SPONGE_OUT              : 1e5
<<end_coef>>
<endproperty>

<beginproperty>
NAME                    : velocity V
UNITS                   : m/s
DIMENSION               : 3D
OUTPUT_HDF              : 1
COLD_RELAX_PERIOD       : 43200.
COLD_ORDER              : 5
<<begin_field>>
DEFAULTVALUE            : 0
INITIALIZATION_METHOD   : HDF
FILE_IN_TIME            : HDF
FIELD4D                 : 1
SPATIAL_INTERPOL        : 1
EXTRAPOLATE             : 1
FILENAME                : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
TYPE_ZUV                : z
<<end_field>>
<<begin_coef>>
DEFAULTVALUE            : 1e5
TYPE_ZUV                : v
FILE_IN_TIME            : NONE
REMAIN_CONSTANT         : 1
INITIALIZATION_METHOD   : SPONGE
SPONGE_OUT              : 1e5
<<end_coef>>
<endproperty>

<beginproperty>
NAME                    : temperature
UNITS                   : °C
DIMENSION               : 3D
OUTPUT_HDF              : 1
COLD_RELAX_PERIOD       : 43200.
COLD_ORDER              : 5
<<begin_field>>
DEFAULTVALUE            : 20
INITIALIZATION_METHOD   : HDF
FILE_IN_TIME            : HDF
FIELD4D                 : 1
SPATIAL_INTERPOL        : 1
EXTRAPOLATE             : 1
FILENAME                : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
TYPE_ZUV                : z
<<end_field>>
<<begin_coef>>
DEFAULTVALUE            : 1e5
TYPE_ZUV                : z
FILE_IN_TIME            : NONE
REMAIN_CONSTANT         : 1
INITIALIZATION_METHOD   : SPONGE
SPONGE_OUT              : 1e5
<<end_coef>>
<endproperty>

<beginproperty>
NAME                    : salinity
UNITS                   : °C
DIMENSION               : 3D
OUTPUT_HDF              : 1
COLD_RELAX_PERIOD       : 43200.
COLD_ORDER              : 5
<<begin_field>>
DEFAULTVALUE            : 36
INITIALIZATION_METHOD   : HDF
FILE_IN_TIME            : HDF
FIELD4D                 : 1
SPATIAL_INTERPOL        : 1
EXTRAPOLATE             : 1
FILENAME                : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
TYPE_ZUV                : z
<<end_field>>
<<begin_coef>>
DEFAULTVALUE            : 1e5
TYPE_ZUV                : z
FILE_IN_TIME            : NONE
REMAIN_CONSTANT         : 1
INITIALIZATION_METHOD   : SPONGE
SPONGE_OUT              : 1e5
<<end_coef>>
<endproperty>
"""
    

def template_waterproperties(start_date):
    return f"""
OUTPUT_TIME                  : 0  3600.
RESTART_FILE_OUTPUT_TIME     : 0  86400.
RESTART_FILE_OVERWRITE       : 1
WRITE_CONTINUOUS_FORMAT      : 1
READ_CONTINUOUS_FORMAT       : 1
SIMPLE_OUTPUT                : 1
ADV_METHOD_H                 : 4
TVD_LIMIT_H                  : 4
ADV_METHOD_V                 : 4
TVD_LIMIT_V                  : 4

LW_EXTINCTION_TYPE           : 1
LW_EXTINCTION_COEF           : 3
LW_PERCENTAGE                : 0.4
SW_EXTINCTION_COEF           : 0.071428571
SW_PERCENTAGE                : 0.6

<beginproperty>
NAME                         : salinity
UNITS                        : psu
DESCRIPTION                  : Salinity
IS_COEF                      : 1
INITIALIZATION_METHOD        : HDF
FIELD4D                      : 1
SPATIAL_INTERPOL             : 1
EXTRAPOLATE                  : 1
FILENAME                     : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
DEFAULTVALUE                 : 36.
DEFAULTBOUNDARY              : 36.
BOUNDARY_INITIALIZATION      : INTERIOR
BOUNDARY_CONDITION           : 4   
COLD_RELAX_PERIOD            : 43200.
DATA_ASSIMILATION            : 1
ADVECTION_DIFFUSION          : 1
ADVECTION_V_IMP_EXP          : 0
ADVECTION_H_IMP_EXP          : 1 
DIFFUSION_V_IMP_EXP          : 0
SCHMIDT_COEF_V               : 1
SCHMIDT_BACKGROUND_V         : 0
OUTPUT_HDF                   : 1
<endproperty>

<beginproperty>
NAME                         : temperature
UNITS                        : °C
DESCRIPTION                  : temperature
IS_COEF                      : 1
PARTICULATE                  : 0
INITIALIZATION_METHOD        : HDF
FIELD4D                      : 1
SPATIAL_INTERPOL             : 1
EXTRAPOLATE                  : 1
FILENAME                     : ..\..\\bc_hdf5\cmems_{start_date}.hdf5
DEFAULTVALUE                 : 19.
DEFAULTBOUNDARY              : 19.
BOUNDARY_INITIALIZATION      : INTERIOR
BOUNDARY_CONDITION           : 4 
COLD_RELAX_PERIOD            : 43200.
DATA_ASSIMILATION            : 1
ADVECTION_DIFFUSION          : 1
ADVECTION_V_IMP_EXP          : 0
ADVECTION_H_IMP_EXP          : 1 
DIFFUSION_V_IMP_EXP          : 0
SCHMIDT_COEF_V               : 1
SCHMIDT_BACKGROUND_V         : 0
OUTPUT_HDF                   : 1
<endproperty>
"""


def template_nomfich(today_date):
    return f"""
IN_BATIM                      : ..\GeneralData\Bathymetry\BIG_L01.dat
ROOT                          : ..\L01\\res\\
ROOT_SRT                      : ..\L01\\res\Run1\\
IN_MODEL                      : ..\L01\data\Model_1.dat
SURF_DAT                      : ..\L01\data\Atmosphere_1.dat
SURF_HDF                      : ..\L01\\res\Atmosphere_1.hdf
DOMAIN                        : ..\L01\data\Geometry_1.dat
DISCHARG                      : ..\L01\data\Discharges_1.dat
AIRW_DAT                      : ..\L01\data\InterfaceWaterAir_1.dat
AIRW_HDF                      : ..\L01\\res\InterfaceWaterAir_1.hdf
AIRW_FIN                      : ..\L01\\res\InterfaceWaterAir_1.fin
AIRW_INI                      : ..\L01\\res\InterfaceWaterAir_0.fin
BOT_DAT                       : ..\L01\data\InterfaceSedimentWater_1.dat
BOT_HDF                       : ..\L01\\res\InterfaceSedimentWater_1.hdf
BOT_FIN                       : ..\L01\\res\InterfaceSedimentWater_1.fin
BOT_INI                       : ..\L01\\res\InterfaceSedimentWater_0.fin
IN_DAD3D                      : ..\L01\data\Hydrodynamic_1.dat
OUT_DESF                      : ..\..\\results\Hydrodynamic_{today_date}.hdf
OUT_FIN                       : ..\L01\\res\Hydrodynamic_1.fin
IN_CNDI                       : ..\L01\\res\Hydrodynamic_0.fin
IN_TURB                       : ..\L01\data\Turbulence_1.dat
TURB_HDF                      : ..\L01\\res\Turbulence_1.hdf
DISPQUAL                      : ..\L01\data\WaterProperties_1.dat
EUL_HDF                       : ..\..\\results\WaterProperties_{today_date}.hdf
EUL_FIN                       : ..\L01\\res\WaterProperties_1.fin
EUL_INI                       : ..\L01\\res\WaterProperties_0.fin
FREE_DAT                      : ..\L01\data\Free Vertical Movement_1.dat
WQDATA                        : ..\L01\data\WaterQuality_1.dat
BENTHOS_DATA                  : ..\L01\data\Benthos_1.dat
ASSIMILA_DAT                  : ..\L01\data\Assimilation_1.dat
ASSIMILA_HDF                  : ..\L01\\res\Assimilation_1.hdf
TURB_GOTM                     : ..\L01\data\GOTM_1.dat
TURB_FIN                      : ..\L01\\res\GOTM_1.fin
TURB_INI                      : ..\L01\\res\GOTM_0.fin
"""

