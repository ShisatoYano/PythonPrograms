# -*- coding: utf-8 -*-
"""
create model and predict label of origine wine

using Linear SVC(SVM Classification) of Scikit Learn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing, metrics
from mlxtend.plotting import plot_decision_regions

def normalize_split_data(data_frame, normalize_mode):
    '''Normalize and split sample data
        Input1: Original data frame
        Input2: Normalize mode number
            1: Original
            2: z score normalization
            3: Min-Max normalization
        
        Output1: Attributes data for training
        Output2: Attributes data for test
        Output3: Label data for training
        Output4: Label data for test
    '''
    data_label      = data_frame['Class'].values
    data_attrib_org = data_frame[['Color intensity', 'Proline']].values

    if normalize_mode == 1: # Original
        attrib_train, attrib_test, label_train, label_test = train_test_split(data_attrib_org, data_label, test_size=0.4, random_state=3)
    elif normalize_mode == 2: # z score normalization
        sc              = preprocessing.StandardScaler()
        data_attrib_std = sc.fit_transform(data_attrib_org)
        attrib_train, attrib_test, label_train, label_test = train_test_split(data_attrib_std, data_label, test_size=0.4, random_state=3)
    elif normalize_mode == 3: # Min-Max normalization
        ms              = preprocessing.MinMaxScaler()
        data_attrib_nrm = ms.fit_transform(data_attrib_org)
        attrib_train, attrib_test, label_train, label_test = train_test_split(data_attrib_nrm, data_label, test_size=0.4, random_state=3)
    else:
        attrib_train, attrib_test, label_train, label_test = train_test_split(data_attrib_org, data_label, test_size=0.4, random_state=3)
    return attrib_train, attrib_test, label_train, label_test 

def main():
    wine_data_frame = pd.read_csv('wine_data_frame.csv')

    attrib_train, attrib_test, label_train, label_test = normalize_split_data(wine_data_frame, normalize_mode=3)

    # Create Instance
    linear_svc = LinearSVC(loss='hinge', C=1.0, class_weight='balanced', random_state=0)

    # Create Prediction model
    clf_result = linear_svc.fit(attrib_train, label_train)

    # prediction
    label_pred = clf_result.predict(attrib_test)

    # Calculate Prediction Accuracy
    accuracy_score = metrics.accuracy_score(label_test, label_pred)

    # Dispay training/test results
    fig_rst_trn_tst, (ax_rst_trn, ax_rst_tst) = plt.subplots(1,2,figsize=(7,7))
    plot_decision_regions(attrib_train, label_train, clf=clf_result, ax=ax_rst_trn, res=0.01, legend=2)
    plot_decision_regions(attrib_test, label_test, clf=clf_result, ax=ax_rst_tst, res=0.01, legend=2)
    ax_rst_trn.set_title('Left:Train data result, Right:Test data result')
    ax_rst_tst.set_title(['Accuracy: ' + str(accuracy_score)])
    ax_rst_trn.grid()
    ax_rst_tst.grid()
    fig_rst_trn_tst.tight_layout() 

    plt.show()

if __name__ == '__main__':
    main()