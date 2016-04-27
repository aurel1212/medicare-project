""" Functions for cleaning provider drug aggregate data. """

import pandas as pd
import numpy as np
import psycopg2 as pg2
from sklearn import linear_model

def sql_query_read(table_name, dbname='medicare', user='postgres'):
    """ Reads in data from postgres via sql query and returns df

    Parameters
    ----------
    table_name : string
        name of table to read in
    dbname : string
        name of sql database
    user : string
        postgres user name

    Returns
    -------
    df : pandas df

    Examples
    --------
    """
    query = '''
            SELECT *
            FROM {};
            '''.format(table_name)
    conn = pg2.connect(dbname=dbname, user=user)
    df = pd.read_sql_query(query, conn)

    return df


def specialty_avg_cost(col_claim, col_specialty, df):
    """
    Computes the average cost of drugs per specialty
    Returns original data frame with column added

    Parameters
    ----------
    col_claim : list of strings
        first part of column names to be computed
    col_specialty : string
        name of column with the specialty descriptions
    df : pandas df
        data frame containing data

    Returns
    -------
    df : pandas df
        original data frame with additional column 'col_claim_avg' \
        with the average cost per claim for that row's specialty

    Examples
    --------
    """
    df_cost = df_npi[['{}_cost'.format(col_claim), col_specialty]].groupby(col_specialty).sum()
    df_count = df_npi[['{}_count'.format(col_claim), col_specialty]].groupby(col_specialty).sum()
    avg_cost = df_cost.divide(np.array(df_count), axis=1)
    avg_cost.fillna(np.mean(avg_cost), inplace=True)
    
    return pd.merge(df, avg_cost, how='inner', left_on=col_specialty, right_index=True, suffixes=('','_avg'))


def impute_claim_cost(col_claim, col_specialty, df):
    """
    Imputes claim costs for all nulls in a column

    Parameters
    ----------
    col_claim : string
        first part of column names to be computed
    col_specialty : string
        name of column with the specialty descriptions
    df : pandas df
        data frame containing data

    Returns
    -------
    df : pandas df
        data frame with columns imputed

    Examples
    --------
    """
    df = specialty_avg_cost(col_claim, col_specialty, df)
    fill_count_null(col_claim+'_count', df)
    mask = df['{}_cost'.format(col_claim)].isnull()
    df['{}_cost'.format(col_claim)][mask] = \
       df['{}_count'.format(col_claim)][mask] * df[mask].iloc[:,-1]
    
    return df

def fill_count_null(col_claim, df):
    """
    Imputes claim counts for all nulls in a column.
    Set to 5.5 temporarily. May be modified in the future.

    Parameters
    ----------
    col_claim : string
        column name to be computed
    df : pandas df
        data frame containing data

    Returns
    -------
    none : modified in place

    Examples
    --------
    """
    VALUE = 5.5
    df[col_claim].fillna(VALUE, inplace=True)


def linear_impute(col_null_name, col_model_name, df):
    """
    Imputes claim counts for all nulls in a column using a linear model.
    Not used at this time, imputes values well over 10.

    Parameters
    ----------
    col_null_name : strings
        full column name of column to be imputed
    col_model_name : string
        full column name of column to model on (dependent)
    df : pandas df
        data frame containing data

    Returns
    -------
    lin_mod : fitted linear model
        data frame is modified in place

    Examples
    --------
    """
    x_train = df[col_model_name][-df[col_null_name].isnull()]
    y_train = df[col_null_name][-df[col_null_name].isnull()]
    
    x_test = df[col_model_name][df[col_null_name].isnull()]
    x_nulls = df[col_null_name][df[col_null_name].isnull()]

    lin_mod = linear_model.LinearRegression(normalize=True, fit_intercept=True)
    lin_mod.fit(x_train.reshape(len(x_train), 1), y_train.reshape(len(y_train), 1))
    df[col_null_name][df[col_null_name].isnull()] = lin_mod.predict(x_test.reshape(len(x_test), 1))
    
    return lin_mod


def feature_engineer_drug_agg(df):
    #total cost per claim
    df['tot_cost_per_claim'] = df['total_drug_cost']. / df['total_claim_count']
    #total cost per day
    df['total_cost_per_day'] = df['total_drug_cost']. / df['total_day_supply']
    #generic to brand claim count
    df['generic_brand_count_ratio'] = df['generic_claim_count']. / (df['brand_claim_count']+df['generic_claim_count']
    #generic to brand claim cost
    df['generic_brand_cost_ratio'] = df['generic_claim_cost']. / (df['brand_claim_cost']+df['generic_claim_cost'])
    #brand to total claim ratio
    df['brand_total_claim_ratio'] = df['brand_claim_count']. / df['total_claim_count']
    #replace infinite with 1
    #df.replace(np.inf, 1, inplace=True)


def null_flag(df, col):
    df[col] = [1 if n is None else 0 for n in df[col]]
    df[col] = df[col].astype('category')

def normalize_numerics(df, normalize_col):
    numerics = ['int64', 'float64']
    for col in df[1:]:
        if df[col].dtypes in numerics:
            df[col+'_norm'] = df[col] / df[normalize_col]


