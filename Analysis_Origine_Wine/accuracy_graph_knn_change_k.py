# -*- coding: utf-8 -*-
"""
create model and predict label of origine wine.

using K Nearest Neighbor Class of Scikit Learn.

accuracy plot by changing k.
"""

from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn import metrics

def split_data_train_test(data_frame):
    data_label      = data_frame['Class'].values
    #data_attributes = data_frame.ix[:,1:].values
    data_attributes = data_frame[['Color intensity', 'Proline']].values
    attrib_train, attrib_test, label_train, label_test = train_test_split(data_attributes,data_label,test_size=0.4,random_state=3)

    label_train_1 = label_train[label_train == 1]
    label_train_2 = label_train[label_train == 2]
    label_train_3 = label_train[label_train == 3]
    print('Lbl Trn 1 Num:%d, Lbl Trn 2 Num:%d, Lbl Trn 3 Num:%d' % (len(label_train_1), len(label_train_2), len(label_train_3)))

    print('Attrib Train Num:%d, Label Train Num:%d' % (len(attrib_train), len(label_train)))
    print('Attrib Test Num:%d, Label Test Num:%d' % (len(attrib_test), len(label_test)))

    return attrib_train, attrib_test, label_train, label_test

def main():
    wine_data_frame = pd.read_csv('wine_data_frame.csv')

    attrib_train, attrib_test, label_train, label_test = split_data_train_test(wine_data_frame)

    accuracy     = []
    k_append     = []
    max_k        = 1
    max_accuracy = 0

    # Changing parameter k
    for k in tqdm(range(1, 90)):
        # Create Instance
        knn = KNeighborsClassifier(n_neighbors=k)

        # Create Prediction model
        knn.fit(attrib_train, label_train)

        # prediction
        label_pred = knn.predict(attrib_test)

        # Calculate Prediction Accuracy
        accuracy_score = metrics.accuracy_score(label_test, label_pred)

        # append accuracy
        accuracy.append(accuracy_score)
        k_append.append(k)

        # update max accuracy
        if accuracy_score > max_accuracy:
            max_accuracy = accuracy_score
            max_k        = k

    # plot accuracy graph
    plt.plot(k_append, accuracy)
    plt.title(['Max Accuracy[%]:' + str(max_accuracy*100) + ', Max K:' + str(max_k)])
    plt.grid()

    plt.show()

if __name__ == '__main__':
    main()