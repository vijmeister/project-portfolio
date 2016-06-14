# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 21:04:40 2015

@author: Vijay
"""
import pandas as pd
import __future__
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_curve, accuracy_score, classification_report
from matplotlib import pyplot as plt
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import time
from sklearn.metrics import matthews_corrcoef
#import xgboost as xgb
start_time = time.time()
#read summary data
path='C:\\Users\\Vijay\\Documents\\train_directory.csv'
path1='C:\\Users\\Vijay\\Documents\\test_directory.csv'

path2='C:\\Users\\Vijay\\Documents\\train_pivot.csv'
path3='C:\\Users\\Vijay\\Documents\\test_pivot.csv'

#train_directory=pd.read_csv(path)
#test_directory=pd.read_csv(path1)

train=pd.read_csv(path2)
test=pd.read_csv(path3)

#splitting into training and test datasets
is_test = np.random.uniform(0, 1, len(train)) > 0.70
train_ = train[is_test==False]
test_ = train[is_test==True]
train_.dtypes
#plot the roc curve           
def plot_ml(name, probs):
    precision, recall, thresholds = precision_recall_curve(test_['TripType'], probs)
    plt.clf()
    plt.plot(recall, precision, 'r--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(name)
    plt.legend(loc="lower right")
    plt.show()

#classifiers with features

cols=["ScanCount","DepartmentDescription","Count","Weekday"]

'''clfs = [    
    ("KNN", KNeighborsClassifier()),
    ("NB", GaussianNB()),
    ("CART",DecisionTreeClassifier()),
    ('RandomForest', RandomForestClassifier()),
    ('BaggingKNN', BaggingClassifier(KNeighborsClassifier())),
    ('BaggingRandomForest', BaggingClassifier(RandomForestClassifier())),
    ('BaggingCART', BaggingClassifier(DecisionTreeClassifier())),
    ("GBC",GradientBoostingClassifier())
    ]'''

table=[]
  
'''for name, clf in clfs:
    clf.fit(train_[cols], train_["TripType"])
    clf.predict(test_[cols])
    preds = clf.predict_proba(test_[cols])
    #print(confusion_matrix(test['class'], clf.predict(test[cols])))
    print (pd.crosstab(test_['TripType'], clf.predict(test_[cols]), rownames=["Actual"], colnames=["Predicted"]))
    print (classification_report(test_['TripType'], clf.predict(test_[cols])))
    score=accuracy_score(test_['TripType'],clf.predict(test_[cols]))
    table.append([name,score])
print (table)
'''
clf=BaggingClassifier(GradientBoostingClassifier())
clf.fit(train_[cols], train_["TripType"])
clf.predict(test_[cols])
preds = clf.predict_proba(test_[cols])
#print(confusion_matrix(test['class'], clf.predict(test[cols])))
print (pd.crosstab(test_['TripType'], clf.predict(test_[cols]), rownames=["Actual"], colnames=["Predicted"]))
print (classification_report(test_['TripType'], clf.predict(test_[cols])))
score=accuracy_score(test_['TripType'],clf.predict(test_[cols]))
table.append([score])
print (table)

eclf = VotingClassifier(estimators = [('BaggingKNN', BaggingClassifier(KNeighborsClassifier(20))),
    ('RandomForest', RandomForestClassifier(10)),
    ('BaggingCART', BaggingClassifier(DecisionTreeClassifier()))],
    voting='soft', weights=[7,1,1])
eclf.fit(train[cols], train["TripType"])
#use the classifier to predict
predicted=eclf.predict(test[cols])
#print (accuracy_score(predicted,test['TripType']))
#print(classification_report(predicted,test['TripType']))

'''
OvR = OneVsRestClassifier(BaggingClassifier((LogisticRegression()))).fit(train_[cols], train_["TripType"])
predicted = OvR.predict(test_[cols])
print accuracy_score(predicted,test_['TripType'])

rf = RandomForestClassifier()
rf.fit(train_[cols], train_["TripType"])
predicted = rf.predict(test_[cols])
print accuracy_score(predicted,test_['TripType'])

ada = AdaBoostClassifier()
ada.fit(train_[cols], train_["TripType"])
predicted = ada.predict(test_[cols])
print accuracy_score(predicted,test_['TripType'])
'''
test["TripType"]=predicted

test_piv=pd.pivot_table(test, values=['ScanCount'], columns='TripType', index=['VisitNumber'], aggfunc=np.count_nonzero)
test_piv= test_piv.fillna(0)
'''columns_=[]
columns_=test_piv.columns
print(columns_[[1]])
for i in range(0,37):
    columns_.append(test_piv.columns[i](1))
#test_piv = test_piv.ix[1:]
test_piv.columns=str(test_piv.levels[1])'''
test.to_csv(path_or_buf='C:\\Users\\Vijay\\Documents\\test_new.csv')
test_piv.to_csv(path_or_buf='C:\\Users\\Vijay\\Documents\\test_p_new.csv')

print("--- %s seconds ---" % (time.time() - start_time))