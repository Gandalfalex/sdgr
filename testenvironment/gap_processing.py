import numpy as np
from scipy.interpolate import UnivariateSpline


def find_differences_in_steps_and_fill_them_with_nan(train_data, timestamps_normalized):
    # TODO make the 0.01 something globally accessible
    """
    Identifies gaps in the timestamp data and fills the corresponding positions in the train data with NaN values.
    The gaps are identified based on the differences between consecutive timestamps. If the difference is significantly
    larger than the minimum difference, it is considered a gap.

    :param train_data: List of numpy arrays, where each array represents a set of training data.
    :param timestamps_normalized: List of numpy arrays, where each array represents normalized timestamps corresponding to the training data.
    :return: A numpy array of processed training data with NaN values inserted at the positions of the gaps.
    """
    percentage = 0.01
    processed_train_data = []
    processed_time_stamps = []
    for i, (train_d, timestamp_d) in enumerate(zip(train_data, timestamps_normalized)):
        differences = np.diff(timestamp_d)
        # threshold should not be lower than the minimum value (add 1% to account for error)
        threshold = differences.min() + differences.min() * percentage
        # find all gaps that are larger than the threshold and get the starting and ending indices
        large_gap_indices = np.where(differences > threshold)[0]
        first_elements_of_gaps = large_gap_indices
        second_elements_of_gaps = large_gap_indices + 1
        # calculate gap size
        diff = np.ceil(-(differences[second_elements_of_gaps] - differences[first_elements_of_gaps]) / threshold)

        new_timestamps = np.copy(timestamp_d)
        new_train_d = np.copy(train_d)
        # fill the array with nan at missing values
        for index, size in sorted(zip(second_elements_of_gaps, diff), key=lambda x: x[0], reverse=True):
            nan_array = np.full(int(np.round(size)), np.nan)
            new_timestamps = np.insert(new_timestamps, index, nan_array)

            # Assuming you want to insert the same value in train_data as in the previous position
            # value_to_insert = new_train_d[index - 1]
            # value_array = np.full(int(np.round(size)), value_to_insert)
            new_train_d = np.insert(new_train_d, index, nan_array)

        processed_train_data.append(new_train_d)
        processed_time_stamps.append(new_timestamps)
    return np.array(processed_train_data), np.array(processed_time_stamps)


def categorize_gaps(data_sets):
    """
    Finds all NaN elements in the input data and saves the starting index and the length of the NaN sequence.

    :param data_sets: List of numpy arrays, where each array represents a set of data.
    :return: List of sets, where each set contains tuples (start position, length) of the NaN sequences in the corresponding data set.
    """
    gaps = []
    for data in data_sets:
        isnan = np.isnan(data)
        isnan_padded = np.concatenate(([False], isnan, [False]))

        # Step 2: Find where the True values change to False and vice versa
        change_points = np.diff(isnan_padded.astype(int))  # Convert to int for proper subtraction

        # Step 3: Find start and end indices of nan sequences
        nan_starts = np.where(change_points == 1)[0]
        nan_ends = np.where(change_points == -1)[0]

        # Step 4: Calculate lengths of nan sequences
        lengths = nan_ends - nan_starts
        gap_sets = list(zip(nan_starts, lengths))
        for i, y in enumerate(gap_sets):
            print(f"gap: {i}, found values: {data[y[0]: y[0] + y[1]]}")
            print(f"look beyond gap: {data[y[0] - 1]} and {data[y[0] + y[1] + 1]}")
        gaps.append(gap_sets)
    return gaps


def handle_gaps(data_elements, gaps_elements, imputation_algorithm, large_gap_value = 0):
    # TODO make the 0.10 something globally accessible
    """
    Handle gaps in data sets.

    If the gap in a data set is larger than 10% of the original data -> large gap, fill with zeros
    Else fill the gap with the provided imputation algorithm.

    :param data_elements: List of 1D numpy arrays with data
    :param gaps_elements: List of sets with (start position, length) of the gaps
    :param imputation_algorithm: Function to impute missing values in small gaps
    :return: List of 1D numpy arrays with gaps handled
    """

    percentage = 0.10
    handled_data = []

    for i, (data, gaps_of_data) in enumerate(zip(data_elements, gaps_elements)):
        # Copy data to avoid modifying the original array
        data = np.copy(data)
        # lambda to revers order, start from the end to remove shifting

        context_max = 100
        for j in range(1, len(gaps_of_data)):
            context_max = min(context_max,
                              (gaps_of_data[j][0] - (gaps_of_data[j - 1][0] + gaps_of_data[j - 1][1])) if j > 0 else
                              gaps_of_data[j][0])

        for gap in sorted(gaps_of_data, key=lambda x: x[0], reverse=True):

            start, length = gap
            if (len(data) * percentage) < length:
                # Large gap: fill with zeros
                data[start:start + length] = large_gap_value
            else:
                # Small gap: fill with imputation algorithm
                context_start = max(0, start - context_max)
                context_end = min(len(data), start + length + context_max)
                data[context_start:context_end] = imputation_algorithm(data[context_start:context_end])

        handled_data.append(data)

    return handled_data


def mean_imputation(arr):
    """
    Perform mean imputation on an array, replacing NaN values with the mean of the array.

    :param arr: 1D numpy array with missing values represented as NaN.
    :return: 1D numpy array with NaN values replaced by the mean of the array.
    """
    mean_val = np.nanmean(arr)
    imputed_arr = np.where(np.isnan(arr), mean_val, arr)
    return imputed_arr


def median_imputation(arr):
    """
    Perform median imputation on an array, replacing NaN values with the median of the array.

    :param arr: 1D numpy array with missing values represented as NaN.
    :return: 1D numpy array with NaN values replaced by the median of the array.
    """
    median_val = np.nanmedian(arr)
    imputed_arr = np.where(np.isnan(arr), median_val, arr)
    return imputed_arr


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
