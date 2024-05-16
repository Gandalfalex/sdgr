from typing import List, Tuple, Callable, Union

import numpy as np

error_percentage = 0.01
gap_size_for_imputation = 0.10


def contains_gaps(time_stamps_normalized: List[np.ndarray]) -> bool:
    """
    look for gaps in the provided list of timestamps.
    :param time_stamps_normalized:
    :return: true if they contain gaps, else false
    """
    for time_stamp in time_stamps_normalized:
        differences = np.diff(time_stamp)
        threshold = differences.min() + differences.min() * error_percentage
        large_gap_indices = np.where(differences > threshold)[0]
        if large_gap_indices.size > 0:
            return True
    return False


def __find_differences_in_steps_and_fill_them_with_nan(train_data: List[np.ndarray],
                                                       timestamps_normalized: List[np.ndarray]) -> Tuple[
    List[np.ndarray], List[np.ndarray]]:
    # TODO make the 0.01 something globally accessible
    """
    Identifies gaps in the timestamp data and fills the corresponding positions in the train data with NaN values.
    The gaps are identified based on the differences between consecutive timestamps. If the difference is significantly
    larger than the minimum difference, it is considered a gap.

    :param train_data: List of numpy arrays, where each array represents a set of training data.
    :param timestamps_normalized: List of numpy arrays, where each array represents normalized timestamps corresponding to the training data.
    :return: A numpy array of processed training data with NaN values inserted at the positions of the gaps.
    """
    processed_train_data = []
    processed_time_stamps = []
    for i, (train_d, timestamp_d) in enumerate(zip(train_data, timestamps_normalized)):
        differences = np.diff(timestamp_d)
        # threshold should not be lower than the minimum value (add 1% to account for error)
        threshold = differences.min() + differences.min() * error_percentage
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

            new_train_d = np.insert(new_train_d, index, nan_array)

        processed_train_data.append(new_train_d)
        processed_time_stamps.append(new_timestamps)
    return processed_train_data, processed_time_stamps


def __categorize_gaps(data_sets: List[np.ndarray]) -> List[List[Tuple[int, int]]]:
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
        gaps.append(gap_sets)
    return gaps


def __handle_gaps(data_elements: List[np.ndarray], gaps_elements: List[List[Tuple[int, int]]],
                  imputation_algorithm: Callable[[np.ndarray], np.ndarray], large_gap_value: Union[int, float] = 0) -> \
        Tuple[List[np.ndarray], bool]:
    # TODO make the 0.10 something globally accessible
    """
    Handle gaps in data sets.

    If the gap in a data set is larger than 10% of the original data -> large gap, fill with zeros
    Else fill the gap with the provided imputation algorithm.

    :param large_gap_value: default 0, value used for gaps
    :param data_elements: List of 1D numpy arrays with data
    :param gaps_elements: List of sets with (start position, length) of the gaps
    :param imputation_algorithm: Function to impute missing values in small gaps
    :return: List of 1D numpy arrays with gaps handled
    """

    handled_data = []
    large_gap_found = False
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
            if (len(data) * gap_size_for_imputation) < length:
                # Large gap: fill with zeros
                data[start:start + length] = large_gap_value
                large_gap_found = True
            else:
                # Small gap: fill with imputation algorithm
                context_start = max(0, start - context_max)
                context_end = min(len(data), start + length + context_max)
                data[context_start:context_end] = imputation_algorithm(data[context_start:context_end])

        handled_data.append(data)

    return handled_data, large_gap_found


def remove_gaps_if_existing(original_data: List[np.ndarray], time_data: List[np.ndarray],
                            imputation_function: Callable[[np.ndarray], np.ndarray]) -> Tuple[
    np.ndarray, np.ndarray, int]:
    """
    Remove gaps in the data if they exist.

    :param original_data: List of numpy arrays, where each array represents a set of original data.
    :param time_data: List of numpy arrays, where each array represents time data corresponding to the original data.
    :param imputation_function: Function to impute missing values.
    :return: Tuple of three elements. The first is a numpy array of filled data, the second is a numpy array of marked
    gaps, and the third is an integer representing the length of the data.
    """
    data, times = __find_differences_in_steps_and_fill_them_with_nan(original_data, time_data)
    gaps = __categorize_gaps(data)

    filled_data, large_gap_found = __handle_gaps(data, gaps, imputation_function)

    # mark large gaps with -1 instead of 0, normalization goes to 0, so they are clearly marked
    filled_time_steps, large_gap_found = __handle_gaps(times, gaps, imputation_function, -1)
    # create an array of 0, 1 where 0 sequences are gaps, 1 are normal values
    marked_gaps = []

    for i in filled_time_steps:
        marked_gaps.append(np.where(i == -1, 0, 1))

    same_length = all(len(arr) == len(marked_gaps[0]) for arr in marked_gaps)
    length = len(min(marked_gaps, key=len))

    # if it's not the same length, normalize it
    if not same_length:
        filled_data = [np.interp(np.linspace(0, len(x) - 1, length), np.arange(len(x)), x).tolist() for x in
                       filled_data]
        marked_gaps = [np.interp(np.linspace(0, len(x) - 1, length), np.arange(len(x)), x).tolist() for x in
                       marked_gaps]

    return np.array(filled_data), np.array(marked_gaps), length
