# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 18:24:46 2016

@author: Vijay
"""

import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, AdaBoostClassifier, BaggingClassifier, GradientBoostingClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve, accuracy_score, classification_report
from matplotlib import pyplot as plt

data=pd.read_csv('results.csv')

#frequency table
#data["Number of Comments"].hist(bins=[0,75,400,1000,1500,2000,2500,4000,9000])

#convert continuous variable to categorical for classification
data["Shares Number Categories"]=pd.cut(data["Shares"],5)

#splitting into training and test datasets
is_test = np.random.uniform(0, 1, len(data)) > 0.70
train_ = data[is_test==False]
test_ = data[is_test==True]

#selecting features

cols=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]

#pick 3 classifiers
clf1 = RandomForestClassifier()
clf2 = BaggingClassifier(GradientBoostingClassifier())
clf3 = BaggingClassifier(LogisticRegression())

#build a voting classifer
eclf = VotingClassifier(estimators=[('RF', clf1), ('BGBM', clf2), ('BLR', clf3)], voting='soft', weights=[5,3,3])

#train all classifier on the same datasets
eclf.fit(train_[cols], train_["Shares Number Categories"])

#use hard voting to predict (majority voting)
pred=eclf.predict(test_[cols])

#print accuracy
print accuracy_score(test_["Shares Number Categories"],eclf.predict(test_[cols]))

#feature importance
clf1.fit(train_[cols], train_["Shares Number Categories"])
importances = clf1.feature_importances_
indices = np.argsort(importances)[::-1]

feat_labels = data.columns[4:-1]
plt.title('Feature Importance')
plt.bar(range(train_[cols].shape[1]),
        importances[indices],
        color='lightblue',
        align='center')
plt.xticks(range(train_[cols].shape[1]),
           feat_labels, rotation=90)
plt.xlim([-1, train_[cols].shape[1]])
plt.tight_layout()
plt.show()

#export predictions
pd.DataFrame(pred).to_csv('predicitions.csv')
#confusion matrix
#print (pd.crosstab(test_["Shares"], eclf.predict(test_[cols]), rownames=["Actual"], colnames=["Predicted"]))

#classification report
#print (classification_report(test_["Comments Number Categories"],clf.predict(test_[cols])))
