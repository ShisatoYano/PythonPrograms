# -*- coding: utf-8 -*-
"""
read nmea sample log as list.
extract $GPGGA data 
"""

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pyproj

sample_file_name = '2005-09-25-north-tahoe_nmea.txt'
gpgga_array = np.empty((0, 15))
date_time_array = np.empty(0)
data_counter = 0

def transform_lonlat_to_xy(gpgga_data_frame):
    # convert lat_deg_min to lat_deg
    lat_dm_array_str   = gpgga_data_frame['Latitude'].values
    lat_dm_array_float = [float(lat_str) for lat_str in lat_dm_array_str] # str -> float
    lat_d_array_int    = [int(lat_dm_float/100) for lat_dm_float in lat_dm_array_float]
    lat_m_array_float  = [(lat_dm_float/100 - lat_d_array_int[idx_lat]) for idx_lat, lat_dm_float in enumerate(lat_dm_array_float)]
    lat_d_array_float  = [lat_m_float*100/60 for lat_m_float in lat_m_array_float]
    lat_d_array        = [(lat_d_array_int[idx_lat]+lat_d_float) for idx_lat, lat_d_float in enumerate(lat_d_array_float)]

    # convert lon_deg_min to lon_deg
    lon_dm_array_str   = gpgga_data_frame['Longitude'].values
    lon_dm_array_float = [float(lon_str) for lon_str in lon_dm_array_str] # str -> float
    lon_d_array_int    = [int(lon_dm_float/100) for lon_dm_float in lon_dm_array_float]
    lon_m_array_float  = [(lon_dm_float/100 - lon_d_array_int[idx_lon]) for idx_lon, lon_dm_float in enumerate(lon_dm_array_float)]
    lon_d_array_float  = [lon_m_float*100/60 for lon_m_float in lon_m_array_float]
    lon_d_array        = [(lon_d_array_int[idx_lon]+lon_d_float) for idx_lon, lon_d_float in enumerate(lon_d_array_float)] 
    
    # transform from grs80 to x-y
    grs80 = pyproj.Proj(init='EPSG:6668')
    rect6 = pyproj.Proj(init='EPSG:6680')
    x_tmp, y_tmp  = pyproj.transform(grs80, rect6, lon_d_array, lat_d_array)
    # North:+, South:-
    north_south = gpgga_data_frame['North/South'].values
    y = [-y_tmp[idx_n_e] if n_or_e == 'S' else y_tmp[idx_n_e] for idx_n_e, n_or_e in enumerate(north_south)]
    # East:+, West:-
    east_west = gpgga_data_frame['East/West'].values
    x = [-x_tmp[idx_e_w] if e_or_w == 'W' else x_tmp[idx_e_w] for idx_e_w, e_or_w in enumerate(east_west)]
    # add x and y to data frame
    gpgga_data_frame['x'] = x
    gpgga_data_frame['y'] = y
    return gpgga_data_frame

def analyze_plot_gpgga(gpgga_data_frame):
    # extract each data
    x             = gpgga_data_frame['x']
    y             = gpgga_data_frame['y']
    altitude      = gpgga_data_frame['Altitude'] # [m]
    geoid_height  = gpgga_data_frame['Geoid Height'] # [m]
    quality       = gpgga_data_frame['Quality']
    hdop          = gpgga_data_frame['HDOP']
    satellite_num = gpgga_data_frame['Satellites Num']

    # scatter: x, y colored by quality
    fig_xy_qua, ax_xy_qua = plt.subplots(1,1,figsize=(7,7))
    sc_xy_qua = ax_xy_qua.scatter(x, y, c=quality, cmap='spring')
    title_str = 'GPS x-y position colored by quality '
    ax_xy_qua.set_title(title_str) 
    ax_xy_qua.set_xlabel('X')
    ax_xy_qua.set_ylabel('Y')
    ax_xy_qua.grid()
    fig_xy_qua.tight_layout()
    plt.colorbar(sc_xy_qua)

    # scatter: x, y colored by hdop
    fig_xy_hdop, ax_xy_hdop = plt.subplots(1,1,figsize=(7,7))
    sc_xy_hdop = ax_xy_hdop.scatter(x, y, c=hdop, cmap='spring')
    title_str = 'GPS x-y position colored by HDOP '
    ax_xy_hdop.set_title(title_str) 
    ax_xy_hdop.set_xlabel('X')
    ax_xy_hdop.set_ylabel('Y')
    ax_xy_hdop.grid()
    fig_xy_hdop.tight_layout()
    plt.colorbar(sc_xy_hdop)

    # scatter: x, y colored by satellite num
    fig_xy_satnum, ax_xy_satnum = plt.subplots(1,1,figsize=(7,7))
    sc_xy_satnum = ax_xy_satnum.scatter(x, y, c=satellite_num, cmap='spring')
    title_str = 'GPS x-y position colored by Satellite Num'
    ax_xy_satnum.set_title(title_str) 
    ax_xy_satnum.set_xlabel('X')
    ax_xy_satnum.set_ylabel('Y')
    ax_xy_satnum.grid()
    fig_xy_satnum.tight_layout()
    plt.colorbar(sc_xy_satnum)

    # scatter: x, y colored by altitude
    fig_xy_altitude, ax_xy_altitude = plt.subplots(1,1,figsize=(7,7))
    sc_xy_altitude = ax_xy_altitude.scatter(x, y, c=altitude, cmap='spring')
    title_str = 'GPS x-y position colored by Altitude'
    ax_xy_altitude.set_title(title_str) 
    ax_xy_altitude.set_xlabel('X')
    ax_xy_altitude.set_ylabel('Y')
    ax_xy_altitude.grid()
    fig_xy_altitude.tight_layout()
    plt.colorbar(sc_xy_altitude)

    # scatter: x, y colored by Geoid height
    fig_xy_geo, ax_xy_geo = plt.subplots(1,1,figsize=(7,7))
    sc_xy_geo = ax_xy_geo.scatter(x, y, c=geoid_height, cmap='spring')
    title_str = 'GPS x-y position colored by Geoid height'
    ax_xy_geo.set_title(title_str) 
    ax_xy_geo.set_xlabel('X')
    ax_xy_geo.set_ylabel('Y')
    ax_xy_geo.grid()
    fig_xy_geo.tight_layout()
    plt.colorbar(sc_xy_geo)

    plt.show()

def main():
    global gpgga_array
    global date_time_array
    global data_counter

    with open(sample_file_name, 'r') as f:
        str_nmea_log = f.readlines()
    
    file_name_split = sample_file_name.split('-')

    # read NMEA log and extract $GPGGA
    for log_line in tqdm(str_nmea_log):
        if log_line.find('GPGGA') != -1:
            data_counter += 1
            log_line_split = log_line.split(',')
            if data_counter == 1:
                date_time_str = file_name_split[0]+'-'+file_name_split[1]+'-'+file_name_split[2]+\
                                '-'+log_line_split[1]
                init_date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d-%H%M%S')
                date_time_array = np.append(date_time_array, np.array([init_date_time]), axis=0)
                gpgga_array = np.append(gpgga_array, np.array([log_line_split]), axis=0)
                prev_date_time = init_date_time
            else:
                date_time = prev_date_time + datetime.timedelta(seconds=2)
                date_time_array = np.append(date_time_array, np.array([date_time]), axis=0)
                gpgga_array = np.append(gpgga_array, np.array([log_line_split]), axis=0)
                prev_date_time = date_time

    # create DataFrame of GPGGA
    gpgga_format = ['Data Type','UTC Time','Latitude','North/South','Longitude',
                    'East/West','Quality','Satellites Num','HDOP','Altitude','Alit Unit',
                    'Geoid Height','Geo Unit','Comm Time','Check Sum']
    gpgga_data_frame = pd.DataFrame(data=gpgga_array, index=date_time_array, columns=gpgga_format)

    gpgga_data_frame_xy = transform_lonlat_to_xy(gpgga_data_frame)

    gpgga_data_frame_xy.to_csv('nmea_gpgga_data_frame.csv')

    analyze_plot_gpgga(gpgga_data_frame_xy)
    

if __name__ == "__main__":
    main()