import numpy as np


def median_imputation(arr):
    """
    Perform median imputation on an array, replacing NaN values with the median of the array.

    :param arr: 1D numpy array with missing values represented as NaN.
    :return: 1D numpy array with NaN values replaced by the median of the array.
    """
    median_val = np.nanmedian(arr)
    imputed_arr = np.where(np.isnan(arr), median_val, arr)
    return imputed_arr
