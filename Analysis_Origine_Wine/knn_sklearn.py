# -*- coding: utf-8 -*-
"""
create model and predict label of origine wine

using K Nearest Neighbor Class of Scikit Learn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from mlxtend.plotting import plot_decision_regions

def split_data_train_test(data_frame):
    data_label      = data_frame['Class'].values
    # data_attributes = data_frame.ix[:,1:].values
    data_attributes = data_frame[['Color intensity', 'Proline']].values
    attrib_train, attrib_test, label_train, label_test = train_test_split(data_attributes,data_label,test_size=0.4,random_state=3)
    return attrib_train, attrib_test, label_train, label_test

def main():
    wine_data_frame = pd.read_csv('wine_data_frame.csv')

    attrib_train, attrib_test, label_train, label_test = split_data_train_test(wine_data_frame)

    # Create Instance
    knn = KNeighborsClassifier(n_neighbors=20)

    # Create Prediction model
    clf_result = knn.fit(attrib_train, label_train)

    # prediction
    label_pred = clf_result.predict(attrib_test)

    # Calculate Prediction Accuracy
    accuracy_score = metrics.accuracy_score(label_test, label_pred)

    print(accuracy_score)

    # plot trained data
    plot_decision_regions(attrib_train, label_train, clf=clf_result, res=0.01, legend=2)
    # plot test data
    # plot_decision_regions(attrib_test_plot, label_test_plot, clf=clf_result, res=0.01, legend=2)

    plt.show()

if __name__ == '__main__':
    main()