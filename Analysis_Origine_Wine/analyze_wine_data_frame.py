# -*- coding: utf-8 -*-
"""
read DataSet.txt as csv
data is converted to pandas data frame
save the data frame as csv file
"""

import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

def plot_2d_correlation(data_frame):
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

def scatter_2d_correlation(data_frame):
    wine_class     = data_frame['Class']
    wine_flava     = data_frame['Flavanoids']
    wine_dilu      = data_frame['OD280/OD315 of diluted wines']
    wine_tophen    = data_frame['Total phenols']
    wine_hue       = data_frame['Hue']
    wine_proline   = data_frame['Proline']
    wine_clr_intns = data_frame['Color intensity']

    df_cls_clr_pln = data_frame[['Class', 'Color intensity', 'Proline']]

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

    sbn.pairplot(df_cls_clr_pln, hue='Class')

    plt.show()

def compare_origine_standard_normalize(data_frame):
    # original data
    data_label      = data_frame['Class'].values
    data_attrib_org = data_frame[['Color intensity', 'Proline']].values

    # standard
    sc              = preprocessing.StandardScaler()
    data_attrib_std = sc.fit_transform(data_attrib_org)

    # normalize
    ms              = preprocessing.MinMaxScaler()
    data_attrib_nrm = ms.fit_transform(data_attrib_org)

    # distribution of Proline and Color intensity
    fig_hist_prl_cint, (ax_hist_prl, ax_hist_cint) = plt.subplots(1,2,figsize=(7,7))
    ax_hist_cint.hist(data_attrib_org[:,0], bins=20)
    ax_hist_prl.hist(data_attrib_org[:,1], bins=20)
    ax_hist_cint.set_title('Histgram of Color intensity distribution')
    ax_hist_prl.set_title('Histgram of Proline distribution')
    ax_hist_cint.grid()
    ax_hist_prl.grid()
    fig_hist_prl_cint.tight_layout()

    # Proline - Color intensity Scatter: original
    fig_prl_cint_org, ax_prl_cint_org = plt.subplots(1,1,figsize=(7,7))
    sc_prl_cint_org = ax_prl_cint_org.scatter(data_attrib_org[:,0], data_attrib_org[:,1], vmin=1, vmax=3, c=data_label, cmap='spring')
    title_str = 'Wine Correlation(Org): Proline - Color intensity colored by Class'
    ax_prl_cint_org.set_title(title_str) 
    ax_prl_cint_org.set_ylabel('Proline(Org)')
    ax_prl_cint_org.set_xlabel('Color intensity(Org)')
    ax_prl_cint_org.grid()
    fig_prl_cint_org.tight_layout()
    plt.colorbar(sc_prl_cint_org)

    # Proline - Color intensity Scatter: standard
    fig_prl_cint_std, ax_prl_cint_std = plt.subplots(1,1,figsize=(7,7))
    sc_prl_cint_std = ax_prl_cint_std.scatter(data_attrib_std[:,0], data_attrib_std[:,1], vmin=1, vmax=3, c=data_label, cmap='spring')
    title_str = 'Wine Correlation(Std): Proline - Color intensity colored by Class'
    ax_prl_cint_std.set_title(title_str) 
    ax_prl_cint_std.set_ylabel('Proline(Std)')
    ax_prl_cint_std.set_xlabel('Color intensity(Std)')
    ax_prl_cint_std.grid()
    fig_prl_cint_std.tight_layout()
    plt.colorbar(sc_prl_cint_std)

    # Proline - Color intensity Scatter: normalization
    fig_prl_cint_nrm, ax_prl_cint_nrm = plt.subplots(1,1,figsize=(7,7))
    sc_prl_cint_nrm = ax_prl_cint_nrm.scatter(data_attrib_nrm[:,0], data_attrib_nrm[:,1], vmin=1, vmax=3, c=data_label, cmap='spring')
    title_str = 'Wine Correlation(Nrm): Proline - Color intensity colored by Class'
    ax_prl_cint_nrm.set_title(title_str) 
    ax_prl_cint_nrm.set_ylabel('Proline(Nrm)')
    ax_prl_cint_nrm.set_xlabel('Color intensity(Nrm)')
    ax_prl_cint_nrm.grid()
    fig_prl_cint_nrm.tight_layout()
    plt.colorbar(sc_prl_cint_nrm)

    plt.show()

def integrate_class1_class3(data_frame):
    data_frame_intg = data_frame
    wine_class_intg = data_frame_intg['Class']
    for idx_class, class_num in enumerate(wine_class_intg):
        if class_num == 3:
            wine_class_intg[idx_class] = 1
    data_frame_intg['Class'] = wine_class_intg
    return data_frame_intg

def main():
    wine_data_frame = pd.read_csv('wine_data_frame.csv')

    # wine_data_frame_intg = integrate_class1_class3(wine_data_frame)

    # plot_2d_correlation(wine_data_frame_intg)

    # scatter_2d_correlation(wine_data_frame)

    compare_origine_standard_normalize(wine_data_frame)

if __name__ == '__main__':
    main()