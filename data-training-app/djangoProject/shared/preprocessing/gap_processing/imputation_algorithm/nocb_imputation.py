import numpy as np


def nocb_imputation(arr):
    """
    Perform Next Observation Carried Backward (NOCB) imputation on an array,
    replacing NaN values with the next observed value.

    :param arr: 1D numpy array with missing values represented as NaN.
    :return: 1D numpy array with NaN values replaced using NOCB imputation.
    """
    imputed_arr = np.copy(arr)
    for i in range(len(arr) - 2, -1, -1):
        if np.isnan(imputed_arr[i]):
            imputed_arr[i] = imputed_arr[i + 1]
    return imputed_arr
