# -*- coding: utf-8 -*-
"""
read DataSet.txt as csv
data is converted to pandas data frame
save the data frame as csv file
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split

def plot__2d_correlation(data_frame):
    wine_class = data_frame['Class']
    for colmun in data_frame.columns:
        if colmun != 'Class':
            wine_feature = data_frame[colmun]
            fig_cor, ax_plt_cor = plt.subplots(1,1,figsize=(7,7))
            ax_plt_cor.plot(wine_feature, wine_class, '.', c='#2196F3')
            title_str = 'Wine Correlation: ' + colmun + ' - Class'
            ax_plt_cor.set_title(title_str) 
            ax_plt_cor.set_xlabel(colmun)
            ax_plt_cor.set_ylabel('Class')
            ax_plt_cor.set_ylim([0, 4])
            ax_plt_cor.grid()
            fig_cor.tight_layout()
    plt.show()

def scatter__2d_correlation(data_frame):
    wine_class     = data_frame['Class']
    wine_flava     = data_frame['Flavanoids']
    wine_dilu      = data_frame['OD280/OD315 of diluted wines']
    wine_tophen    = data_frame['Total phenols']
    wine_hue       = data_frame['Hue']
    wine_proline   = data_frame['Proline']
    wine_clr_intns = data_frame['Color intensity']
    # scatter: each attributions - class
    # for colmun in data_frame.columns:
    #     if colmun != 'Class' and colmun != 'Color intensity':
    #         wine_feature = data_frame[colmun]
    #         fig_cor, ax_plt_cor = plt.subplots(1,1,figsize=(7,7))
    #         sc = ax_plt_cor.scatter(wine_feature, wine_class, c=wine_clr_intns, cmap='spring')
    #         title_str = 'Wine Correlation: ' + colmun + ' - Class'
    #         ax_plt_cor.set_title(title_str) 
    #         ax_plt_cor.set_xlabel(colmun)
    #         ax_plt_cor.set_ylabel('Class')
    #         ax_plt_cor.set_ylim([0, 4])
    #         ax_plt_cor.grid()
    #         fig_cor.tight_layout()
    #         plt.colorbar(sc)

    # scatter colored by class
    # 1: Flavanoids - Color intensity
    fig_flav_intns, ax_flav_intns = plt.subplots(1,1,figsize=(7,7))
    sc_flav_intns = ax_flav_intns.scatter(wine_flava, wine_clr_intns, vmin=1, vmax=3, c=wine_class, cmap='spring')
    title_str = 'Wine Correlation: Flavanoids - Color intensity colored by Class'
    ax_flav_intns.set_title(title_str) 
    ax_flav_intns.set_xlabel('Flavanoids')
    ax_flav_intns.set_ylabel('Color intensity')
    ax_flav_intns.grid()
    fig_flav_intns.tight_layout()
    plt.colorbar(sc_flav_intns)

    # 2: Diluted - Color intensity
    fig_dilu_intns, ax_dilu_intns = plt.subplots(1,1,figsize=(7,7))
    sc_dilu_intns = ax_dilu_intns.scatter(wine_dilu, wine_clr_intns, vmin=1, vmax=3, c=wine_class, cmap='spring')
    title_str = 'Wine Correlation: OD280/OD315 of diluted wines - Color intensity colored by Class'
    ax_dilu_intns.set_title(title_str) 
    ax_dilu_intns.set_xlabel('OD280/OD315 of diluted wines')
    ax_dilu_intns.set_ylabel('Color intensity')
    ax_dilu_intns.grid()
    fig_dilu_intns.tight_layout()
    plt.colorbar(sc_dilu_intns)

    # 3: Total phenols - Color intensity
    fig_tophen_intns, ax_tophen_intns = plt.subplots(1,1,figsize=(7,7))
    sc_tophen_intns = ax_tophen_intns.scatter(wine_tophen, wine_clr_intns, vmin=1, vmax=3, c=wine_class, cmap='spring')
    title_str = 'Wine Correlation: Total phenols - Color intensity colored by Class'
    ax_tophen_intns.set_title(title_str) 
    ax_tophen_intns.set_xlabel('Total phenols')
    ax_tophen_intns.set_ylabel('Color intensity')
    ax_tophen_intns.grid()
    fig_tophen_intns.tight_layout()
    plt.colorbar(sc_tophen_intns)

    # 4: Hue - Color intensity
    fig_hue_intns, ax_hue_intns = plt.subplots(1,1,figsize=(7,7))
    sc_hue_intns = ax_hue_intns.scatter(wine_hue, wine_clr_intns, vmin=1, vmax=3, c=wine_class, cmap='spring')
    title_str = 'Wine Correlation: Hue - Color intensity colored by Class'
    ax_hue_intns.set_title(title_str) 
    ax_hue_intns.set_xlabel('Hue')
    ax_hue_intns.set_ylabel('Color intensity')
    ax_hue_intns.grid()
    fig_hue_intns.tight_layout()
    plt.colorbar(sc_hue_intns)

    # 5: Proline - Color intensity
    fig_proline_intns, ax_proline_intns = plt.subplots(1,1,figsize=(7,7))
    sc_proline_intns = ax_proline_intns.scatter(wine_proline, wine_clr_intns, vmin=1, vmax=3, c=wine_class, cmap='spring')
    title_str = 'Wine Correlation: Proline - Color intensity colored by Class'
    ax_proline_intns.set_title(title_str) 
    ax_proline_intns.set_xlabel('Proline')
    ax_proline_intns.set_ylabel('Color intensity')
    ax_proline_intns.grid()
    fig_proline_intns.tight_layout()
    plt.colorbar(sc_proline_intns)

    plt.show()

def integrate_class1_class3(data_frame):
    data_frame_intg = data_frame
    wine_class_intg = data_frame_intg['Class']
    for idx_class, class_num in enumerate(wine_class_intg):
        if class_num == 3:
            wine_class_intg[idx_class] = 1
    data_frame_intg['Class'] = wine_class_intg
    return data_frame_intg

def split_data_train_test(data_frame):
    data_label      = data_frame['Class'].values
    data_attributes = data_frame.ix[:,1:].values
    attrib_train, attrib_test, label_train, label_test = train_test_split(data_attributes,data_label,test_size=0.3,random_state=0)
    return label_train, attrib_train

def main():
    wine_data_frame = pd.read_csv('wine_data_frame.csv')

    # label_train, attrib_train = split_data_train_test(wine_data_frame)

    # wine_data_frame_intg = integrate_class1_class3(wine_data_frame)

    # plot__2d_correlation(wine_data_frame_intg)

    scatter__2d_correlation(wine_data_frame)

if __name__ == '__main__':
    main()