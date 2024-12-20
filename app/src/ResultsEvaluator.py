import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.svm import SVC,LinearSVC
from sklearn import preprocessing
import numpy as np

from matplotlib.figure import Figure

class EvaluateResults():

    def __init__(self, af):
        self.af = af
        self.features = []
        self.labels = []
        self.X_train= []
        self.X_test= []
        self.y_train= []
        self.y_test = []


    def get_features_and_labels(self):
        self.features, self.labels = self.af.get_features_and_labels()
        print(len(self.labels))


    def show_label_distribution(self):

        label_count = np.count_nonzero(self.labels)
        non_label_count = len(self.labels) - label_count
        width = 0.25

        fig = Figure(figsize=(2, 3),layout='constrained')
        ax= fig.subplots()
        rects= ax.bar('not angry',non_label_count,width)
        ax.bar_label(rects, label_type='edge')

        rects= ax.bar('angry',label_count,width)
        ax.bar_label(rects, label_type='edge')

        ax.set_title('Distribution of labels')
        ax.tick_params(axis='y',labelsize=7)
        ax.tick_params(axis='y',labelsize=7)
        ax.title.set_size(10)
        #ax.set_xticks(x+width,xlabels)
        ax.set_ylim(0, 1500)
        return self.af.fig_to_buf(fig)




    def scale_features(self):
        self.features = StandardScaler().fit_transform(self.features)

    def encode_labels(self):
        self.labels = preprocessing.LabelEncoder().fit_transform(self.labels)
    
    def split_dataset(self, test_size=0.2):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features,
            self.labels,
            test_size=test_size)
        
    def get_train_metrics(self,model, features,_labels):
        # obtain scores
        model.fit(features,_labels)
        scoring = ['recall','precision','accuracy']
        scores = cross_validate(model, features, _labels,scoring=scoring,cv=5)
        return scores
    
    def arrange_scores(self, res):
        num_tests = len(res['test_recall'])
        arr2D = []
        for i in range(num_tests):
            row = [round(res['test_recall'][i],2), round(res['test_precision'][i],2),round(res['test_accuracy'][i],2)]
            arr2D.append(row)
        return arr2D


    def get_SVC_scores(self):
        svc = SVC(
            C = 1.0,
            gamma='auto',
            class_weight='balanced',
            kernel='rbf')

        scores = self.get_train_metrics(svc, self.X_train,self.y_train)  
        return self.arrange_scores(scores)
    
    def get_LinearSVC_scores(self):
        linear_svc = LinearSVC(
            C = 1.0,
            class_weight='balanced',
            fit_intercept=False)
        
        scores = self.get_train_metrics(linear_svc, self.X_train,self.y_train)
        return self.arrange_scores(scores)