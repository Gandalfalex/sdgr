import numpy as np
from scipy.interpolate import UnivariateSpline


def spline_interpolate(arr, k=2, s=None):
    """
    Perform spline interpolation on a 1D array with missing values.

    :param arr: 1D numpy array with missing values represented as nan
    :param k: Degree of the smoothing spline. Must be <= 5. Default is k=3, a cubic spline.
    :param s: Positive smoothing factor used to choose the number of knots. Number of knots
              will be increased until the smoothing condition is satisfied:
              sum((w[i] * (y[i]-g(x[i])))**2, axis=0) <= s
              If None (default), s = len(w) which should be a good value if 1/w[i] is an estimate of
              the standard deviation of y[i].
    :return: 1D numpy array with missing values interpolated
    """
    x = np.arange(len(arr))
    mask = np.isnan(arr)

    xs = x[~mask]
    ys = arr[~mask]

    spline = UnivariateSpline(xs, ys, k=k, s=s)
    arr_interpolated = spline(x)

    return arr_interpolated