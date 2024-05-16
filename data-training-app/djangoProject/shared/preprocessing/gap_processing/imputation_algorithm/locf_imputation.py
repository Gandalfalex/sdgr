import numpy as np


def locf_imputation(arr):
    """
    Perform Last Observation Carried Forward (LOCF) imputation on an array,
    replacing NaN values with the last observed value.

    :param arr: 1D numpy array with missing values represented as NaN.
    :return: 1D numpy array with NaN values replaced using LOCF imputation.
    """
    imputed_arr = np.copy(arr)
    for i in range(1, len(arr)):
        if np.isnan(imputed_arr[i]):
            imputed_arr[i] = imputed_arr[i - 1]
    return imputed_arr
