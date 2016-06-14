# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:00:43 2015

@author: Vijay
"""

import pandas as pd
import numpy as np
from scipy.stats import mode
import calendar

#reading test and training files
train=pd.read_csv('C:\\Users\\Vijay\\Documents\\train.csv')
test=pd.read_csv('C:\\Users\\Vijay\\Documents\\test.csv')

#cleaning null values
train=train.fillna(0)
test=test.fillna(0)

#convert weekdays to numbers: from Stackexchange
#http://stackoverflow.com/questions/4482050/python-converting-monday-tuesday-wednesday-to-monday-to-wednesday
day_indexes = {name:i for i, name in enumerate(calendar.day_name)}
indexes = [day_indexes[d] for d in train['Weekday']]
train['Weekday']=indexes
day_indexes = {name:i for i, name in enumerate(calendar.day_name)}
indexes = [day_indexes[d] for d in test['Weekday']]
test['Weekday']=indexes

#mapping of fineline number, upc to dept description
train_directory=pd.pivot_table(train, values=['FinelineNumber','Upc'], index=['DepartmentDescription'])
test_directory=pd.pivot_table(test, values=['FinelineNumber','Upc'], index=['DepartmentDescription'])

#convert Dept Description to index
#creating a Dictionary mapping department name to index
l = list(train_directory.index)
dept_indices = {}
num = 0
for x in l:
    dept_indices[x] = num
    num += 1
indices= [dept_indices[d] for d in train['DepartmentDescription']]
train['DepartmentDescription']=indices

indices= [dept_indices[d] for d in test['DepartmentDescription']]
test['DepartmentDescription']=indices

#basket size
p_table1=pd.pivot_table(train, values='ScanCount', index=['VisitNumber'], aggfunc=np.count_nonzero)
p_table1t=pd.pivot_table(test, values='ScanCount', index=['VisitNumber'], aggfunc=np.count_nonzero)

#department that most items fall under
p_table=pd.pivot_table(train, values='DepartmentDescription', index=['VisitNumber'], aggfunc=mode)
p_tablet=pd.pivot_table(test, values='DepartmentDescription', index=['VisitNumber'], aggfunc=mode)

#weekdays the trips occur
p_table3=pd.pivot_table(train,values=['Weekday','TripType'], index=['VisitNumber'])
p_table3t=pd.pivot_table(test,values=['Weekday','TripType'], index=['VisitNumber'])

#combining the first two pivot tables
p_table1_df=pd.DataFrame(p_table1,columns=['ScanCount'])
p_table3_df=pd.DataFrame(p_table3,columns=['Weekday','TripType'])
p_table1_dft=pd.DataFrame(p_table1t,columns=['ScanCount'])
p_table3_dft=pd.DataFrame(p_table3t,columns=['Weekday','TripType'])

p_table_list=list(p_table)
p_table_listt=list(p_tablet)

#formatting cells to remove embedded tuples and arrays
p_table_df=pd.DataFrame(p_table_list,columns=['DepartmentDescription','Count'],index=p_table1_df.index)
for row in range(0,len(p_table_df)):
    for col in range(0,2):
        i=int(p_table_df.irow(row)[[col]])
        p_table_df.irow(row)[[col]]=i

p_table_dft=pd.DataFrame(p_table_listt,columns=['DepartmentDescription','Count'],index=p_table1_dft.index)
for row in range(0,len(p_table_dft)):
    for col in range(0,2):
        i=int(p_table_dft.irow(row)[[col]])
        p_table_dft.irow(row)[[col]]=i

train_pivot=pd.concat([p_table1_df,p_table_df,p_table3_df],axis=1,ignore_index=False)
test_pivot=pd.concat([p_table1_dft,p_table_dft,p_table3_dft],axis=1,ignore_index=False)

#exporting tables
train_directory.to_csv(path_or_buf='C:\\Users\\Vijay\\Documents\\train_directory.csv')
test_directory.to_csv(path_or_buf='C:\\Users\\Vijay\\Documents\\test_directory.csv')

train_pivot.to_csv(path_or_buf='C:\\Users\\Vijay\\Documents\\train_pivot.csv')
test_pivot.to_csv(path_or_buf='C:\\Users\\Vijay\\Documents\\test_pivot.csv')