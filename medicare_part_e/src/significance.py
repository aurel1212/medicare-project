import numpy as np 
import pandas as pd 
import scipy.stats as scs
from itertools import combinations

def sig_test(clustA, clustB, num_tests):
    """
    calculate z score for two proportions with null hypothesis of no difference.
    input: np array of prop, count of clusters to be compared
    """
    total_prop = (clustA[0]*clustA[1] + clustB[0]*clustB[1]) / (clustA[1]+clustB[1])
    zscore = scs.norm.ppf(.05/num_tests)*((total_prop) * (1-total_prop)*(1 / clustA[0] + 1 / clustB[0]))**0.5

    return zscore

def col_sig_test(df_prop_col, df_count_col, comb=2, num_tests=3):
    zipped = zip(df_prop_col.values, df_count_col.values)
    zscore = []
    for i in combinations(zipped, comb):
        zscore.append(sig_test(i[0], i[1], num_tests))

    return pd.DataFrame(zscore)

def run_sig_test(df_prop, df_count, comb=2, num_tests=3):
    """
    runs z test on all possible pairs
    input - data frame with cluster designation as index and comparison categories as columns
    output - data frame with combination pairs as index, comparison categories as columns and 
    z score as values
    """
    df = df_prop.copy()
    for i in range(df_prop.shape[1]):
        df.iloc[:,i] = col_sig_test(df_prop.iloc[:,i], df_count.iloc[:,i], comb, num_tests)

    return df


