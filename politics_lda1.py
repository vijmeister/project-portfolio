# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:30:52 2016

@author: Vijay
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import lda
import numpy as np

#read file
#path='C:/Users/Vijay/Downloads/politics.csv'

file_=pd.read_csv('politics_m.csv')

#read the dataset                
docs=open('articles_m2.txt').readlines()

#remove na

#file_=file_.dropna()
#file_=file_.reset_index()

topic_num=20

#tokenization
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')

#transform the docs into a count matrix
matrix = tf_vectorizer.fit_transform(docs)

#get the vocabulary
vocab=tf_vectorizer.get_feature_names()

#initialize the LDA model
model = lda.LDA(n_topics=topic_num, n_iter=500)

#fit the model to the dataset
model.fit(matrix)

#write the top terms for each topic
top_words_num=20
topic_mixes= model.topic_word_
fw=open('top_terms_per_topic.txt','w')
for i in range(topic_num):#for each topic
    sorted_indexes=np.argsort(topic_mixes[i])[len(topic_mixes[i])-top_words_num:]#get the indexes of the top-k terms in this topic
    sorted_indexes=sorted_indexes[::-1]#reverse to get the best first    
    my_top=''
    for ind in sorted_indexes:my_top+=vocab[ind]+' ' 
    fw.write('TOPIC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()


#write the top topics for each doc
top_topics_num=3
doc_mixes= model.doc_topic_
fw=open('topic_mixture_per_doc.txt','w')
for i in range(len(doc_mixes)):#for each doc
    sorted_indexes=np.argsort(doc_mixes[i])[len(doc_mixes[i])-top_topics_num:]#get the indexes of the top-k topics in this doc
    sorted_indexes=sorted_indexes[::-1]#reverse to get the best first    
    my_top=''
    for ind in sorted_indexes:my_top+=' '+str(ind)+':'+str(round(doc_mixes[i][ind],2))
    fw.write('DOC: '+str(i)+' --> '+str(my_top)+'\n')
    
fw.close()

#combining mixture array with original dataframe
result = pd.concat([file_, pd.DataFrame(doc_mixes[1:,:])], axis=1)
result.to_csv('results.csv')