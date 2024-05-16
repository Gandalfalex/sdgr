import numpy as np


def mean_imputation(arr):
    """
    Perform mean imputation on an array, replacing NaN values with the mean of the array.

    :param arr: 1D numpy array with missing values represented as NaN.
    :return: 1D numpy array with NaN values replaced by the mean of the array.
    """
    mean_val = np.nanmean(arr)
    imputed_arr = np.where(np.isnan(arr), mean_val, arr)
    return imputed_arr
