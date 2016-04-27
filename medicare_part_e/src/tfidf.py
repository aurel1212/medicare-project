""" Takes a list of NPI.
Pulls from psql the service codes and performs tfidf, returning importance vector
"""
import pandas as pd
import numpy as np
import psycopg2 as pg2
import string
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def get_psql(npi_list):
    """
    retrieves hcpcs descriptions from a psql database

    Input:
    list of npi identifiers

    Output:
    dictionary with npi as key and a list of hcpcs descriptions
    """

    npi_dict = {}
    conn = pg2.connect(dbname='medicare', user='postgres')
    cur = conn.cursor()

    for dr in npi_list:
        query = "SELECT hcpcs_desc FROM util_payments_2013 WHERE npi='{0}';".format(dr)
        cur.execute(query)
        npi_dict[dr] = cur.fetchall()
        
    return npi_dict

def flatten_dic(desc_list):
    """
    takes values from one entry of dictionary and flattens
    """
    corp_list = [desc for c in desc_list for desc in c]
    return ' '.join(corp_list)


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    table = string.maketrans("","")
    text = text.translate(table, string.punctuation)
    tokens = word_tokenize(text)
 
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
 
    return tokens 

def perform_tfidf(npi_list, tfidf=False):
    """ Runs TFIDF process """
    npi_dict = get_psql(npi_list)
    corpus = []
    for dr in npi_list:
        corpus.append(flatten_dic(npi_dict[dr]))

    #corpus = [desc for c in corpus for desc in c]
    #corpus = process_text(corpus)
    
    if tfidf:
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=400)
        tfidf_model = vectorizer.fit_transform(corpus)
        return tfidf_model, vectorizer, corpus
    else:
        vectorizer = CountVectorizer(stop_words='english', ngram_range=(1,2), max_features=400)
        count_model = vectorizer.fit_transform(corpus)
        return count_model, vectorizer, corpus

def view_features(matrix, vectorizer, num_features):
    index = np.argsort(np.sum(matrix.toarray(), axis=0))[::-1][:num_features]
    return np.array(vectorizer.get_feature_names())[index]

