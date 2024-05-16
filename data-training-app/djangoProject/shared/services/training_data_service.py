import json
import math
import os

import numpy as np
import pandas as pd

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from djangoProject.common.default_exceptions.invalid_file_type_exception import InvalidFileTypeException
from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from shared.models import TrainData, JwtUser
from shared.preprocessing.gap_processing.gap_processing import contains_gaps, \
    __find_differences_in_steps_and_fill_them_with_nan, remove_gaps_if_existing
from shared.services.database_service import get_train_data, get_or_create_train_data_file
from shared.strategies.gap_detection_strategy import get_imputation_algorithm_strategy

maxlength = 100
max_file_size = 1048576
date_taxonomy = ['date', 'time', 'timestamp']


def upload_data(file, file_type, name, user):
    """
    Uploads a data file and saves it to the database.

    Args:
        file: The data file to be uploaded.
        file_type: The type of the file (e.g., 'npy', 'json', 'csv').
        name: The name to be assigned to the uploaded file.
        user: The user uploading the file.

    Returns:
        A list of IDs representing the saved data entries.
    """
    ids = []
    file.seek(0, os.SEEK_END)
    if file.tell() > max_file_size:
        raise BadRequestException(f"filesize of {int(file.tell() / 1000)}kb is to large",
                                  "files larger than 10mb will be rejected")
    file.seek(0)

    match file_type:
        case "npy":
            ids = __load_numpy(file, user, name)
        case "json":
            ids = __load_json(file, user, name)
        case "csv":
            ids = __load_csv(file, user, name)
    return ids


def reduce(data_list: list):
    """
    Reduces the size of the data list to a specified maximum length.

    Args:
        data_list: A list of data items to be reduced.

    Returns:
        A list of data items reduced to the specified maximum length.

    """
    data = []
    for i in data_list:
        array = [float("{:.2f}".format(i.time_series_value[val])) for val in
                 range(0, len(i.time_series_value),
                       math.floor(len(i.time_series_value) / min(len(i.time_series_value), maxlength)))]
        data.append({
            "name": i.name,
            "values": array
        })
    return data


def get_training_data_by_ids(ids, user):
    """
    Retrieves training data records by their IDs.

    Args:
        ids: A list of IDs of the training data records.

    Returns:
        A list of TrainData objects corresponding to the provided IDs.
    """
    data = [get_train_data(i, user) for i in ids]
    return data


def check_data_and_set_train_data(data: {}, train_data: TrainData):
    data = convert_data_in_valid_format_if_required(data)
    train_data.time_series_value = data.get("value")
    train_data.time_stamp_value = data.get("time")
    return train_data


def build_data_to_interest(pk, user):
    """
    Builds and returns data of interest for a specific training data record.

    Args:
        pk: The primary key of the training data record.
        user: The user associated with the training data.

    Returns:
        A dictionary containing the original and processed data.
    """
    train_model = get_train_data(pk, user)
    x, y = train_model.time_series_value, train_model.time_stamp_value
    x, y = [np.array(x)], [np.array(y)]

    altered_flag = []
    preview = [x[0]]
    if contains_gaps(y):
        imputation = get_imputation_algorithm_strategy("MEDIAN")
        temp_data, temp_times = __find_differences_in_steps_and_fill_them_with_nan(x, y)
        preview, preview_stamps, length = remove_gaps_if_existing(x, y, imputation)
        altered_flag = [True if math.isnan(float(i)) else False for i in temp_data[0]]

    send_data = {
        "original": {"name": "original", "values": preview[0]},
        "flags": altered_flag
    }
    return send_data


def convert_data_in_valid_format_if_required(data: {}):
    """
    Checks and ensures that the uploaded data is in the correct format.

    Args:
        data: The data to be checked.

    Returns:
        The data in a corrected format if necessary, otherwise the original data.
    """
    if len(data) != 2:
        print(f"data in wrong format: {data}")
        data = {
            "value": data,
            "time": list(range(0, len(data)))
        }
    return data


def __load_json(element, user, name):
    """
    Loads and processes a JSON file, saving its contents to the database.

    Args:
        element: The JSON file to be processed.
        user: The user uploading the file.
        name: The name to be assigned to the uploaded data.

    Returns:
        A list of IDs representing the saved data entries.
    """
    try:
        data = json.load(element)
        data = check_json_data(data)
        ids = __save_data_dictionary(data, user, name)
        return ids
    except Exception as e:
        raise UnknownErrorException("could not load json data", f"{e}")


def __load_numpy(element, user, name):
    """
    Loads and processes a NumPy file, saving its contents to the database.

    Args:
        element: The NumPy file to be processed.
        user: The user uploading the file.
        name: The name to be assigned to the uploaded data.

    Returns:
        A list of IDs representing the saved data entries.
    """
    try:
        data = np.load(element).tolist()
        data = check_json_data(data)
        ids = __save_data_dictionary(data, user, name)
        return ids
    except Exception as e:
        raise UnknownErrorException("could not load numpy data", f"{e}")


def __load_csv(element, user, name: str):
    """
    Loads and processes a CSV file, saving its contents to the database.

    Args:
        element: The CSV file to be processed.
        user: The user uploading the file.
        name: The name to be assigned to the uploaded data.

    Returns:
        A list of IDs representing the saved data entries.
    """
    try:
        data = __build_dictionary_from_csv(element)
        ids = []
        for k, v in data.items():
            id_value = __save_values(v, user, name, optional_key_name=k)
            ids.append(id_value)
        return ids
    except Exception as e:
        raise UnknownErrorException("could not load csv data", f"{e}")


def __build_dictionary_from_csv(element):
    """
    Processes a CSV file and converts it into a dictionary format.

    Args:
        element: The CSV file to be processed.

    Returns:
        A dictionary where keys are column names and values are column data.
    """
    df = pd.read_csv(element)
    # Step 2: Identify and convert the timestamp column
    timestamp_column = None
    for column in df.columns:
        if any(keyword in column.lower() for keyword in date_taxonomy):
            timestamp_column = column
            break
    if timestamp_column:
        df[timestamp_column] = pd.to_datetime(df[timestamp_column])
        # get unix time from input field in seconds
        df['timestamp'] = df[timestamp_column].astype(np.int64) // 10 ** 9
        timestamp_array = df['timestamp'].to_numpy().tolist()
    else:
        # else every input for each second
        timestamp_array = [i for i in range(len(df.index))]

    arrays_dict = {}

    for key in df.columns:
        if key != timestamp_column:
            # sometimes might contain space, breaks other information
            key_name = key.replace(" ", "")
            numeric_series = pd.to_numeric(df[key], errors='coerce')
            if not numeric_series.isna().any():
                # All values are numeric
                data_array = numeric_series.to_numpy()
                arrays_dict[key_name] = {"value": data_array.tolist(), "time": timestamp_array}
            else:
                print(f"Column '{key_name}' contains non-numeric values and was skipped.")
    return arrays_dict


def check_json_data(data):
    """
    Validates and formats JSON data to ensure it is in the expected structure.

    Args:
        data: The JSON data to be checked.

    Returns:
        Formatted JSON data as a dictionary.
    """
    result = {}
    if isinstance(data, list):
        # list is one dimensional
        if all(isinstance(item, (int, float)) for item in data):
            result["0"] = {"value": data, "time": [i for i in range(len(data))]}

        # list is multi dimensional
        else:
            timestamp_list = [i for i in range(len(data[0]))]
            for sublist in data:
                if isinstance(sublist, list) and is_regular_intervals(sublist):
                    timestamp_list = sublist
                    print("found sublist")
                    break

            for i, v in enumerate(data):
                if timestamp_list != v:
                    result[i] = {"value": v, "time": timestamp_list}
        return result

        # Case 2: JSON data is a dictionary
    elif isinstance(data, dict):
        # find data that is part of taxonomy -> timestamp
        timestamps = [key for key in data.keys() if key in date_taxonomy]
        timestamp_list = []

        # fill timestamp list with initial values
        if len(timestamps) == 0:
            for key, value in data.items():
                if isinstance(value, list) and is_regular_intervals(value):
                    timestamp_list = value
                    break
        else:
            timestamp_list = data[timestamps[0]]

        # build dictionary
        for key, value in data.items():
            if isinstance(value, list) and key not in timestamps and timestamp_list != value:
                result[key] = {"value": value,
                               "time": timestamp_list if len(timestamp_list) > 0 else [i for i in range(len(value))]}

        return result

    else:
        raise InvalidFileTypeException("JSON data must be either a list or a dictionary",
                                       "json file must contain a list or a dictionary")


def is_regular_intervals(lst):
    """
    Checks if a list of numbers has regular intervals, typically used for timestamps.

    Args:
        lst: A list of numeric values to be checked.

    Returns:
        True if the list has regular intervals, False otherwise.
    """
    if len(lst) < 2:
        return False

    intervals = np.diff(lst)
    return np.all(intervals == intervals[0])


def __save_data_dictionary(data: {}, user, name):
    """
    Saves a dictionary of data to the database.

    Args:
        data: A dictionary of data to be saved.
        user: The user associated with the data.
        name: The name to be assigned to the data.

    Returns:
        A list of IDs representing the saved data entries.
    """
    ids = []
    for k, v in data.items():
        id_value = __save_values(v, user, name)
        ids.append(id_value)
    return ids


def __save_values(data: {}, user: JwtUser, file_name: str, optional_key_name:str=""):
    """
    Saves a single set of values to the database.

    Args:
        data: A dictionary of data values to be saved.
        user: The user associated with the data.
        file_name: The name of the file from which the data was sourced.

    Returns:
        The ID of the saved TrainData object.
    """

    train_file = get_or_create_train_data_file(file_name, user)
    name = f"{build_train_data_name(file_name)}_{optional_key_name}"
    train_data = TrainData(user=user, file=train_file, name=name)
    train_data = check_data_and_set_train_data(data, train_data)
    train_data.save()
    return train_data.id


def build_train_data_name(name: str):
    return name.split(".")[0].replace(".", "")
