# -*- coding: utf-8 -*-
"""
Script for plotting gradient vector.
Function f is displayed as contour line.
"""

import numpy as np
import matplotlib.pyplot as plt

# Define Function f
def f(w_0, w_1):
    return w_0 ** 2 + 2 * w_0 * w_1 + 3

# Partial differential of f with respect to w_0
def df_dw_0(w_0, w_1):
    return 2 * w_0 + 2 * w_1

# Partial differential of f with respect to w_1
def df_dw_1(w_0, w_1):
    return 2 * w_0 + 0 * w_1

if __name__ == '__main__':
    # Define parameters
    range_w = 2
    delta_w = 0.25
    w_0     = np.arange(-range_w, range_w + delta_w, delta_w)
    w_1     = np.arange(-range_w, range_w + delta_w, delta_w)
    num_w   = w_0.shape[0]

    # Define grid space of w
    grid_w_0, grid_w_1 = np.meshgrid(w_0, w_1)
    
    # Define output array
    array_f    = np.zeros((len(w_0), len(w_1)))
    array_dw_0 = np.zeros((len(w_0), len(w_1)))
    array_dw_1 = np.zeros((len(w_0), len(w_1)))

    # Calculate output and partial differential of function
    for idx_w_0 in range(num_w):
        for idx_w_1 in range(num_w):
            array_f[idx_w_1, idx_w_0]    = f(w_0[idx_w_0], w_1[idx_w_1])
            array_dw_0[idx_w_1, idx_w_0] = df_dw_0(w_0[idx_w_0], w_1[idx_w_1])
            array_dw_1[idx_w_1, idx_w_0] = df_dw_1(w_0[idx_w_0], w_1[idx_w_1])
    
    # Plot contour line and gradient vector
    plt.figure(figsize=(9, 4))
    plt.subplots_adjust(wspace=0.3)
    # Contour line
    plt.subplot(1, 2, 1)
    cont = plt.contour(grid_w_0, grid_w_1, array_f, 10, colors='k')
    cont.clabel(fmt='%2.0f', fontsize=8)
    plt.xticks(range(-range_w, range_w + 1, 1))
    plt.yticks(range(-range_w, range_w + 1, 1))
    plt.xlim(-range_w - 0.5, range_w + 0.5)
    plt.ylim(-range_w - 0.5, range_w + 0.5)
    plt.xlabel('$w_0$', fontsize=14)
    plt.ylabel('$w_1$', fontsize=14)

    # Gradient vector
    plt.subplot(1, 2, 2)
    plt.quiver(grid_w_0, grid_w_1, array_dw_0, array_dw_1)
    plt.xticks(range(-range_w, range_w + 1, 1))
    plt.yticks(range(-range_w, range_w + 1, 1))
    plt.xlim(-range_w - 0.5, range_w + 0.5)
    plt.ylim(-range_w - 0.5, range_w + 0.5)
    plt.xlabel('$w_0$', fontsize=14)
    plt.ylabel('$w_1$', fontsize=14)

    plt.show()
