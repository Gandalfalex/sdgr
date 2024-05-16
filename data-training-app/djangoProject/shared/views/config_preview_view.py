import csv
import json
import logging
import math

import numpy as np
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from shared.jwt.jwt_authenticate import jwt_authenticated
from shared.preprocessing.data_formatting.processing_builder import ProcessingBuilder
from shared.preprocessing.gap_processing.gap_processing import contains_gaps, \
    __find_differences_in_steps_and_fill_them_with_nan, remove_gaps_if_existing
from shared.response_object_classes import PreviewDataResponse
from shared.services.database_service import get_train_data, get_all_elements_of_file
from shared.services.training_data_service import convert_data_in_valid_format_if_required, __build_dictionary_from_csv
from shared.strategies.gap_detection_strategy import get_imputation_algorithm_strategy


@swagger_auto_schema(
    method='post',
    responses={
        200: 'PreviewDataResponse',
        400: 'Bad Request - Invalid request data',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
@jwt_authenticated
def create(request, user):
    test = None
    try:
        test = json.loads(request.POST.get('train_data', {}))
    except Exception as e:
        logging.info("no traindata provided")

    if test:
        data_id = test.get("train_data", -1)
        file_id = test.get("file", -1)
        data = [np.random.rand(100).tolist(), np.ones(100).tolist()]
        if data_id != -1:
            data = get_train_data(data_id, user)
        elif file_id != -1:
            data = get_all_elements_of_file(file_id, user)[0]
        data = [data.time_series_value, data.time_stamp_value]
    else:
        data = check_for_data(request, user)

    json_data = json.loads(request.POST.get('metadata', {}))


    selected_processing = json_data.get("Processor Type")

    builder = ProcessingBuilder(name=selected_processing)
    builder.set_min_length(json_data["min_length"])
    config_option = json_data["configuration option"]
    if config_option != "default option":
        builder.set_configuration(json_data.get(f"{selected_processing}Option"))
    data_values = convert_data_in_valid_format_if_required(data)
    builder.set_data([data_values[0]])
    builder.set_time_stamp_data([data_values[1]])
    time_series_preprocessing, time_stamp_preprocessing = builder.get_preprocessors()
    preview, conf = time_series_preprocessing.process()
    time_stamps, _ = time_stamp_preprocessing.process()
    altered_flag = []
    if contains_gaps(time_stamps):
        imputation = get_imputation_algorithm_strategy(json_data.get("Imputation_Algorithm"))
        temp_data, temp_times = __find_differences_in_steps_and_fill_them_with_nan(preview, time_stamps)
        preview, preview_stamps, length = remove_gaps_if_existing(preview, time_stamps, imputation)
        altered_flag = [True if math.isnan(float(i)) else False for i in temp_data[0]]

    preview = [float("{:.2f}".format(i)) if not math.isnan(float(i)) else float('nan') for i in preview[0]]
    result = PreviewDataResponse(data_values[0], preview, altered_flag)
    return Response(status=200, data=result.get_data())


def check_for_data(request, user):
    data = []
    if len(request.FILES) != 0:
        data = check_file(request.FILES.getlist("files"))
    if len(data) == 0:
        optional_data = json.loads(request.POST.get("train_data"))
        if optional_data.get("train_data") == -1:
            return [np.random.rand(100).tolist(), np.ones(100).tolist()]
        if not optional_data:
            return Response({"status": "no data provided", "filetypes": ["json", "numpy", "csv"]}, status=400)
        data = get_train_data(optional_data.get("train_data"), user)
        data = [data.time_series_value, data.time_stamp_value]
    return data


def check_file(files):
    try:
        uploaded_file = files[0]
        name = str(uploaded_file)
        data = get_data(name, uploaded_file)
        return data
    except Exception as e:
        logging.info(f"{e}")
    return []


def get_data(name: str, file):
    if name.endswith('.npy'):
        try:
            np_array = np.load(file)
            data = np_array.tolist()
            return data
        except Exception as e:
            logging.error(f"{e}")
            return []
    elif name.endswith('.json'):
        data = json.load(file)
        return data
    elif name.endswith('.csv'):
        data = __build_dictionary_from_csv(file)
        data = next(iter(data.values()))
        return list(data.values())
    raise UnknownErrorException("no data provided",  f"filetypes: json, numpy, csv are supported")

