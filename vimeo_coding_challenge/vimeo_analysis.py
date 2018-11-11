# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:34:00 2018

@author: krisp
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

#import preprocessed_csv
clips_expanded_=pd.read_csv('clips_expanded.csv')
clips_expanded_=clips_expanded_.fillna("")

#get the text fields title, caption, category names
titles=clips_expanded_['title']

captions=clips_expanded_['caption']

categories=clips_expanded_['category_names']

"""
since I am using TF-IDF I can apply a bag of words model,
I can concatenate the titles, captions, categories
"""
titles_captions_categories=titles + " " + captions+ " " + categories
titles_captions_categories.fillna("")

#using a tokenizer
vectorizer = CountVectorizer()

#creating a count matrix
X = vectorizer.fit_transform(titles_captions_categories)

#convert the count matrix to an array
X.toarray()

#TF-IDF Term weighing
from sklearn.feature_extraction.text import TfidfTransformer

transformer = TfidfTransformer(smooth_idf=False)
 
tfidf = transformer.fit_transform(X)

tfidf_array=tfidf.toarray()

#cosine similarity and getting the top 10 similar movies
from sklearn.metrics.pairwise import linear_kernel
cosine_similarities = linear_kernel(tfidf, tfidf)
related_movies_indices = cosine_similarities.argsort()[:-11:-1]

#transpose
related_movies_indices_formatted=np.transpose(related_movies_indices)

#make into a dataframe
rmif=pd.DataFrame(related_movies_indices_formatted)

#get info about related movies
list_of_clips=[14434107, 249393804, 71964690, 78106175, 228236677, 11374425, 93951774, 35616659, 112360862, 116368488]

"""
PURPOSE: 
INPUTS: a list of clip id's, the table to obtain the related clips' info,
the table of indices for the top 10 related movies,the name of the id variable
to search in the table of clip id's
OUTPUT: a json of the related clips of interest with each key being the orginal
clip id being passed in. The values of each key are the information of the top
10 related movies in descending order of relevance

"""
def obtain_related_clips(list_of_clips,table,rmif,field):
    results={}
    
    for clip in list_of_clips:
        clip_index=table[table[field]==clip].index.values
        indices_of_interest=rmif[rmif.index.isin(clip_index)].values.flatten()
        #I used 'records' to make the json object list like and it coincides best with the tabular format
        clips_json=table.take(indices_of_interest).to_json(orient='records',lines=True)
        results[clip]=clips_json
    
    return results
results=obtain_related_clips(list_of_clips,clips_expanded_,rmif,'id')
import json
with open('results.json', 'w') as f:
    json.dump(results,f)
