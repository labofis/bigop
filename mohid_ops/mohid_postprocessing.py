"""
MOHID post processing functions

@author: Douglas Fraga
"""
import os
import numpy as np
import h5py as hdf
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker



def surface_current_map(BASE_DIR,today_date):

    q = 2                                               # Matrix space
    figure_dir = os.path.join(BASE_DIR, 'figures')
    result_dir = os.path.join(BASE_DIR, 'results')
    shp_dir = os.path.join(BASE_DIR, 'mohid_ops\shp')
    
    shp = shapereader.Reader(os.path.join(shp_dir,'linha_de_costa_master.shp'))
    bat = shapereader.Reader(os.path.join(shp_dir,'isobatimetricas_50_100_200.shp'))
    

###############################################################################
# Load hdf5 hydrodynamic file
###############################################################################
    f = hdf.File(os.path.join(result_dir,"Hydrodynamic_"+today_date+".hdf5"), 'r')
    
    font = {'size': 10}
###############################################################################
# Geographic coordinates
###############################################################################
    Lath = f[('Grid/Latitude')][0:-1,0:-1].T
    Lonh = f[('Grid/Longitude')][0:-1,0:-1].T
    
    Lat = f[('Grid/Latitude')][0:-1:q,0:-1:q].T
    Lon = f[('Grid/Longitude')][0:-1:q,0:-1:q].T
    h = -f['Grid/Bathymetry'][:,:]
    h[h == 99] = -7
    h = np.squeeze(h).T
    
    
###############################################################################
# Define Time List
###############################################################################
    idt = [f'000{i}' for i in range(13, 38)]
    
    
    def make_map(projection=ccrs.PlateCarree()):
        fig, ax = plt.subplots(subplot_kw=dict(projection=projection),figsize=[6.4, 3.8],dpi=100)
        gl = ax.gridlines(draw_labels=True)
        gl.xlabels_top = gl.ylabels_right = False
        gl.xlocator = mticker.FixedLocator([-44.6,-44.3, -44.0, -43.7])
        gl.ylocator = mticker.FixedLocator([-23.35,-23.25,-23.15,-23.05,-22.95])
        gl.xlabel_style = gl.ylabel_style = {'size': 8}
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlines = gl.ylines = False
        return fig, ax
    
       
    extent = [-44.79, -43.5, -23.4, -22.87]
    zlim = [-100, 0]
    
    levels = np.linspace(*zlim, 101)
    ticks = np.linspace(*zlim, 11)
    
    
###############################################################################
# Extract data
###############################################################################
    for k, val in enumerate(idt):
        time = f['Time/Time_'+val][:]
        u = f[('Results/velocity U/velocity U_'+val)][0,::q,::q]
        u[u == 0] = np.nan 
        v = f[('Results/velocity V/velocity V_'+val)][0,::q,::q]
        v[v == 0] = np.nan
    
        u = np.squeeze(u).T*100; v = np.squeeze(v).T*100; 
    
    
###############################################################################
# Maps
###############################################################################
        fig, ax = make_map(projection=ccrs.PlateCarree())
        ax.set_extent(extent)
        plt.set_cmap('ocean')
        ca = plt.contourf(Lonh, Lath, h, levels=levels)
               
        Q = plt.quiver(Lon, Lat, u, v, angles='xy', scale_units='xy', scale=500, width = 0.0015)
        plt.quiverkey(Q, 0.79, 0.19, 30, r'$30$', labelpos='E', coordinates='figure', fontproperties=font)
        plt.quiverkey(Q, 0.79, 0.15, 20, r'$20$', labelpos='E', coordinates='figure', fontproperties=font)
        plt.quiverkey(Q, 0.79, 0.11, 10, r'$10$', labelpos='E', coordinates='figure', fontproperties=font)
    
        for record, geometry in zip(shp.records(), shp.geometries()):
            ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor='gray')
            
        for record, geometry in zip(bat.records(), bat.geometries()):
            ax.add_geometries([geometry], ccrs.PlateCarree(), linewidth=1.50,
                              facecolor='none', edgecolor='lightgray')
           
        plt.text(-43.58,-23.13,'50m',color='lightgrey',size=8)
        plt.text(-44.77,-22.92,f'{np.int64(time[2])}/{np.int64(time[1])}/{np.int64(time[0])} {np.int64(time[3])}:00')
        
        cbaxes = fig.add_axes([0.1, 0.15, .5, 0.03])# [horizontal pos, vertical pos (-), espessura da barra, altura da barra]
        cbar = plt.colorbar(ca, cax = cbaxes, ticks=ticks, extend='both', orientation="horizontal",
                            shrink=0.6, label='Profundidade [$m$]')
        cbar.ax.tick_params(labelsize=8)
        fig.text(0.83, 0.05, u'Velocidade [ $cm.s^{-1}}$ ]', ha='center', fontsize=10)
        fig.subplots_adjust(left=0.09, right=0.99, bottom=0.2, top=0.99)
        figure_name = f'big_{k}'
        plt.savefig(os.path.join(figure_dir,figure_name),dpi=fig.dpi)
        
        