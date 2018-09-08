# -*- coding: utf-8 -*-
"""
Animation Player sample with matplotlib GUI

You can playback data as animation.

The animation progress can be controled by slider GUI.

Playback speed can be controled by radio button.

Animation start/stop can be controled by radio button.
"""

from matplotlib.widgets import RadioButtons, Slider
import matplotlib.pyplot as plt
import matplotlib.gridspec as gds
import pandas as pd
import datetime

def update_animation(crnt_date_time, crnt_x, crnt_y, crnt_qly, total_hdop, total_sat):
    global pb_spd_prm

    ax_pos.set_title(crnt_date_time)
    if crnt_qly == 1:
        snd_aln_plot.set_data(crnt_x, crnt_y)
        diff_plot.set_data([], [])
    elif crnt_qly == 2:
        snd_aln_plot.set_data([], [])
        diff_plot.set_data(crnt_x, crnt_y)
    quality_text.set_text('GPS Quality = %d' % (crnt_qly))

    dt_hdop_plot.set_data(pd.to_datetime(total_hdop.index), total_hdop.values)
    ax_hdop.set_title(total_hdop.values[-1])

    dt_sat_plot.set_data(pd.to_datetime(total_sat.index), total_sat.values)
    ax_sat.set_title(total_sat.values[-1])

    plt.pause(0.05 * pb_spd_prm)

if __name__ == '__main__':

    # close all figure window
    plt.close('all')

    # read data frame csv file
    nmea_gpgga_data_frame = pd.read_csv('nmea_gpgga_data_frame.csv', index_col=0)

    # date time index
    date_time_array = pd.to_datetime(nmea_gpgga_data_frame.index)

    # each data array
    x             = nmea_gpgga_data_frame['x']
    y             = nmea_gpgga_data_frame['y']
    altitude      = nmea_gpgga_data_frame['Altitude']
    quality       = nmea_gpgga_data_frame['Quality']
    hdop          = nmea_gpgga_data_frame['HDOP']
    satellite_num = nmea_gpgga_data_frame['Satellites Num']

    # Animation Playback figure window
    fig_anime = plt.figure(figsize=(11, 9))
    gs_anime  = gds.GridSpec(2, 2)
    plt.subplots_adjust(wspace=0.4, hspace=0.7)
    ax_pos  = plt.subplot(gs_anime[:,0]) # axes of X-Y Position
    ax_pos.plot(x, y, c='#212121')
    ax_pos.set_xlabel('X [m]')
    ax_pos.set_ylabel('Y [m]')
    ax_pos.grid()
    ax_pos.axis('equal')
    ax_hdop = plt.subplot(gs_anime[0,1]) # axes of Time-HDOP
    ax_hdop.set_xlim([date_time_array[0], date_time_array[-1]])
    ax_hdop.set_ylim([hdop.min(), hdop.max()])
    ax_hdop.set_xticklabels(date_time_array, rotation=40)
    ax_hdop.set_xlabel('DateTime')
    ax_hdop.set_ylabel('HDOP')
    ax_hdop.grid()
    ax_sat  = plt.subplot(gs_anime[1,1]) # axes of Time-Satellite Num
    ax_sat.set_xlim([date_time_array[0], date_time_array[-1]])
    ax_sat.set_ylim([satellite_num.min(), satellite_num.max()])
    ax_sat.set_xticklabels(date_time_array, rotation=40)
    ax_sat.set_title('DateTime - Satellite Num')
    ax_sat.set_xlabel('DateTime')
    ax_sat.set_ylabel('Satellite Num')
    ax_sat.grid()
    fig_anime.subplots_adjust(left=0.28, bottom=0.2, right=None, top=None)

    # Update plot objects
    quality_text    = ax_pos.text(0.05, 0.8, '', transform=ax_pos.transAxes)
    snd_aln_plot,   = ax_pos.plot([], [], '.', c='#2196F3', ms=15)
    diff_plot,      = ax_pos.plot([], [], '.', c='#f44336', ms=15)
    dt_hdop_plot,   = ax_hdop.plot([], [], c='#2196F3', linewidth=2.0)
    dt_sat_plot,    = ax_sat.plot([], [], c='#2196F3', linewidth=2.0)

    # radio button for setting playback speed
    radio_btn_clr  = 'lightgoldenrodyellow'
    ax_pb_Spd_btn  = plt.axes([0.05, 0.7, 0.1, 0.1], facecolor=radio_btn_clr)
    pb_spd_btn_obj = RadioButtons(ax_pb_Spd_btn, ('Normal', 'X2', 'X1.5', 'X0.75', 'X0.5'))
    global pb_spd_prm
    pb_spd_prm = 1
    # function
    def select_playback_speed(label):
        global pb_spd_prm
        if label == 'Normal':   # 50ms
            pb_spd_prm = 1
        elif label == 'X2':     # 25ms
            pb_spd_prm = 1/2
        elif label == 'X1.5':   # 33ms
            pb_spd_prm = 1/1.5
        elif label == 'X0.75':  # 67ms
            pb_spd_prm = 1/0.75
        elif label == 'X0.5':   # 100ms
            pb_spd_prm = 1/0.5
        else:
            pb_spd_prm = 1
    pb_spd_btn_obj.on_clicked(select_playback_speed)

    # radio button for switching play/stop animation
    ax_srt_stp_btn  = plt.axes([0.05, 0.5, 0.1, 0.1], facecolor=radio_btn_clr)
    srt_stp_btn_obj = RadioButtons(ax_srt_stp_btn, ('Stop', 'Start'))
    global pushed_start
    pushed_start = False
    # function
    def select_start_stop(label):
        global pushed_start
        if label == 'Stop':    # stop playback
            pushed_start = False
        elif label == 'Start': # start playback
            pushed_start = True
        else:
            pushed_start = False
    srt_stp_btn_obj.on_clicked(select_start_stop)

    # slider for controling animation progress
    global start_date_time, end_date_time, roop_count
    len_date_time = len(date_time_array)
    roop_count = 0
    ax_prg_sld  = plt.axes([0.15, 0.01, 0.7, 0.03])
    prg_sld_obj = Slider(ax_prg_sld, 'Date Time', 0, len_date_time-1, valinit=0)
    # function
    def control_animation_progress(slider_value):
        global roop_count
        roop_count = int(slider_value)
    prg_sld_obj.on_changed(control_animation_progress)

    # animation roop
    while roop_count <= len_date_time-1:
        crnt_date_time = date_time_array[roop_count]
        crnt_x   = x[roop_count]
        crnt_y   = y[roop_count]
        crnt_qly = quality[roop_count]
        total_hdop      = hdop[0:roop_count+1]
        total_sat       = satellite_num[0:roop_count+1]
        update_animation(crnt_date_time, crnt_x, crnt_y, crnt_qly, total_hdop, total_sat)
        if pushed_start == True:
            roop_count += 1
        prg_sld_obj.set_val(roop_count)
