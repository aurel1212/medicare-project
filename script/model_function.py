from sklearn.ensemble import IsolationForest
from sklearn.cross_validation import train_test_split
import pandas as pandas
import numpy as np


def make_train_test_dataset(data_df):
    """Returns train/test split dataframes.

    Parameters
    ----------
    data_df : pandas df
        Full dataframe

    Returns
    -------
    X_train, X_test
        split dataframe

    Examples
    --------
    """
    X_train, X_test = train_test_split(data_df, test_size=.5, random_state=13)

    return X_train, X_test


def fit_model(X_train, model_columns, bootstrap=False, max_features=1.0,
              max_samples='auto', n_estimators=100):
    """Returns fitted isolation forest model

    Parameters
    ----------
    X_train : pandas df
        Full dataframe of trainset
    model_columns : list of strings
        Column names to include in model

    Returns
    -------
    model
        trained isolation forest model

    Examples
    --------
    """
    model = IsolationForest(bootstrap=bootstrap, max_features=max_features,
                            max_samples=max_samples, n_estimators=n_estimators, n_jobs=-1,
                            random_state=13, verbose=True)
    model.fit(X_train[model_columns])

    return model


def prediction(test_df, model_columns, model):
    """Returns df of doctors/npi with outlier prediction.

    Parameters
    -----------
    test_df : pandas df
        Dataframe of test split
    model : isolation forest model
        Trained sklearn isolation forest model

    Returns
    ---------
    df : test data frame with prediction

    Examples
    --------
    """
    test_df['prediction'] = model.predict(test_df[model_columns])

    return test_df


def check_labels(label_df, test_df, model_columns):
    """Returns df of doctors/npi with indictment label.

    Parameters
    -----------
    label_df : pandas df
        Dataframe of doctors with indictments
    test_df : pandas df
        Dataframe of test split

    Returns
    ---------
    df : test data frame with label if found in label set

    Examples
    --------
    """
    test_df['indicted'] = [1 if row in list(label_df['npi'])
                           else 0 for row in test_df['npi']]

    return test_df