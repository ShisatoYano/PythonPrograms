# -*- coding: utf-8 -*-
"""
read DataSet.txt as csv
data is converted to pandas data frame
save the data frame as csv file
"""

import pandas as pd

def main():
    wine_data_frame = pd.read_csv('wine_data_frame.csv')

    print(wine_data_frame.corr())

    print(wine_data_frame)

if __name__ == '__main__':
    main()