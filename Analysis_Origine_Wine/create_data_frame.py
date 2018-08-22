# -*- coding: utf-8 -*-
"""
read DataSet.txt as csv
data is converted to pandas data frame
save the data frame as csv file
"""

import pandas as pd

wine_data_set = pd.read_csv('DataSet.txt', header=None)

wine_data_set.columns = ['Class','Alcohol','Malic acid','Ash','Alcalinity of ash',
                         'Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols',
                         'Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines',
                         'Proline']

print(wine_data_set.describe())

print(wine_data_set.isnull().sum())

print(wine_data_set.head())

wine_data_set.to_csv('wine_data_frame.csv', index=False)

