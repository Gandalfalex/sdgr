import logging

import numpy as np
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from djangoProject.common.default_exceptions.invalid_file_type_exception import InvalidFileTypeException
from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from mlAPI.models import TrainData
from shared.jwt.jwt_authenticate import jwt_authenticated
from shared.preprocessing.gap_processing.gap_processing import contains_gaps
from shared.response_object_classes import TrainDataComplexResponse, TrainDataResponse
from shared.services import training_data_service
from shared.services.database_service import get_train_data, can_delete, get_all_elements_of_file, \
    delete_all_elements_of_file, check_file_usage_before_deletion, get_train_data_file
from shared.services.train_file_service import get_train_data_files, get_train_data_of_file
from drf_yasg.utils import swagger_auto_schema
accepted_file_types = ["npy", "json", "csv"]


@api_view(['POST'])
@jwt_authenticated
@swagger_auto_schema(
    operation_description="Uploads data files",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'files': openapi.Schema(type=openapi.TYPE_FILE, description='Files to upload')
        }
    ),
    responses={200: openapi.Response('Upload Successful')}
)
def upload_data(request, user):
    # Check if any file was uploaded
    if not request.FILES:
        logging.info("No files uploaded")
        raise BadRequestException("no files uploaded", f"accepted filetypes are: {accepted_file_types}")

    ids = []
    # Loop through each uploaded file
    for uploaded_file in request.FILES.getlist('files'):
        name = str(uploaded_file)

        # Validate the file extension
        file_type = name.split(".")[1]
        if file_type not in accepted_file_types:
            raise InvalidFileTypeException(f"filetype {file_type} not supported",
                                           f"only {accepted_file_types} are allowed")
        ids.append(training_data_service.upload_data(uploaded_file, file_type, name, user))

    print(ids)
    temp_data = [i for id in ids for i in id]
    print("returned {} ids".format(len(temp_data)))

    return Response(temp_data, status=200)


@api_view(['GET'])
@jwt_authenticated
def get_train_data_request(request, user):
    try:
        train_models = TrainData.objects.filter(user=user)
        data = []
        for model in train_models:
            arr = np.array(model.time_series_value)
            temp = [x for x in list(arr)]
            data_model = TrainDataResponse(model, len(temp))
            response = data_model.get_data()
            if request.GET.get("get_complete_data", "true") == "true":
                response["data"] = temp
            data.append(response)
        return Response(data)
    except TrainData.DoesNotExist as e:
        raise NotFoundException("train data does not exist", str(e))


@api_view(['GET', 'DELETE'])
@jwt_authenticated
def get_specific_train_data(request, user, pk):
    if request.method == 'GET':
        data = training_data_service.build_data_to_interest(pk, user)
        return Response(status=status.HTTP_200_OK, data=data)
    if request.method == "DELETE":
        if can_delete(pk, user.id):
            print("can delete")
            train_element = get_train_data(pk, user.id)
            # only one remaining that is about to be deleted
            f = train_element.file
            print(f)
            if len(get_all_elements_of_file(train_element.file.id, user)) == 1:
                train_element.file.delete()
            get_train_data(pk, user.id).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        print("cannot delete")
        return Response(status=status.HTTP_409_CONFLICT, data={"message": "traindata in use, delete ml and tsd first"})
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
@jwt_authenticated
def get_user_files(request, user):
    if request.method == "GET":
        return Response(status=status.HTTP_200_OK, data=get_train_data_files(user))
    else:
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'DELETE'])
@jwt_authenticated
def get_elements_of_user_file(request, user, pk):
    if request.method == "GET":
        return Response(status=status.HTTP_200_OK, data=get_train_data_of_file(user, pk))
    elif request.method == "DELETE":
        if check_file_usage_before_deletion(pk, user) > 0:
            get_train_data_file(pk, user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise BadRequestException("cannot delete", "element in use")
    else:
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
@jwt_authenticated
def get_train_data_information(request, user, pk):
    train_model = get_train_data(pk, user)
    x, y = train_model.time_series_value, train_model.time_stamp_value
    train_data_info = TrainDataComplexResponse(train_model, user, contains_gaps([np.array(y)]), len(x))
    return Response(train_data_info.get_data())
