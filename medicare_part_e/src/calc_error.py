import pandas as pd 
import numpy as np 

def highest_error(predictions, y_test):
    """
    returns ordered list of index with highest error first
    """
    error = np.abs(np.array(predictions) - np.array(y_test))
    return zip(np.argsort(error)[::-1], error[np.argsort(error)[::-1]])