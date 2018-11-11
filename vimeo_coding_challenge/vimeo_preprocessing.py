# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:58:21 2018

@author: krisp
"""

import pandas as pd
import numpy as np

#file and path names
path='C:\\Users\\krisp\\Documents\\similar-staff-picks-challenge\\'
#clips
clips_fname='similar-staff-picks-challenge-clips.csv'
#categories
categories_fname='similar-staff-picks-challenge-categories.csv'
#clips to categories
clips_categories_fname='similar-staff-picks-challenge-clip-categories.csv'

#creating pandas dataframes of each dataset
clips=pd.read_csv(path+clips_fname)
categories=pd.read_csv(path+categories_fname)
clips_categories=pd.read_csv(path+clips_categories_fname)

"""
clean up the clips table by narrowing it down based on the textual data
to fit the problem definition of just using title, text description
and category to find similar clips
also eliminating redundant index column and 'id' """

clips_cleaned=clips[['id','clip_id','title','caption','thumbnail']]

#adding category

clips_expanded=pd.merge(clips_cleaned,clips_categories,how='left',on=['clip_id'])

#There is no more need for clip_id

del(clips_expanded['clip_id'])

#handle null values for categories
clips_expanded['categories']=clips_expanded['categories'].fillna("")

"""
PURPOSE: get the category names from the categories
INPUTS : a sequence of numerical categories, the table to look in, 
the name of the id variable, the name of the text column
OUTPUT : a substitution of those numbers by the category name upon 
lookup 
"""
def obtain_category_names(cat_num_seq, table,c_id,name):
    cat_names=[]
    #handling strings that are not empty
    if(cat_num_seq!=""):
        cat_num_seq_list=cat_num_seq.split(', ')
        for cat_num in cat_num_seq_list:
            #handling the case if parent category of value of 0 is used
            try:
                cat_name=table[table[c_id]==int(cat_num)][name].values[0]
            except IndexError:
                pass
            else:
                cat_names.append(cat_name)
        
    return cat_names

"""
testing for the first entry of clips expanded:
categories are 2,26 which are 'Animation' and '2D'    
"""

test_case=obtain_category_names('2, 26',categories,'category_id','name')
assert obtain_category_names('2, 26',categories,'category_id','name')==['Animation', '2D']
#no assertion error

#create a 'category names' column the clips_expanded tbale 
#using the obtain_category_names function defined
clips_expanded['category_names']=clips_expanded['categories'].apply(lambda x: obtain_category_names(x,categories,'category_id','name'))

#save the preprocessed results
clips_expanded.to_csv('clips_expanded.csv',index=False)