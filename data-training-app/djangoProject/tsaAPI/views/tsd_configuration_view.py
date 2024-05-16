import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shared.jwt.jwt_authenticate import jwt_authenticated
from tsaAPI import validator
from tsaAPI.serialize_db import TSDConfigurationSerializer
from tsaAPI.services.tsd_config_service import TsdConfigService

config_service = TsdConfigService()


@swagger_auto_schema(
    method='get',
    responses={
        200: TSDConfigurationSerializer(many=True),
        500: 'Internal Server Error - Something went wrong'
    }
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Configuration request data',
    ),
    responses={
        200: TSDConfigurationSerializer(),
        400: 'Bad Request - Invalid request body',
        500: 'Internal Server Error - Something went wrong'
    }
)
@api_view(['POST', 'GET'])
@jwt_authenticated
def config(request, user, tsd_id):
    if request.method == 'GET':
        data = config_service.get_configs(tsd_id, user=user)
        return Response(status=status.HTTP_200_OK, data=data)

    elif request.method == 'POST':
        res = {}
        if request.body is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="request body needed")
        try:
            req = __convert_body(request)

        except Exception as e:
            logging.info(f"could not decode request {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=res)

        if validator.validate_tsd_config_builder(req):
            data = config_service.create_config(req, tsd_id, user=user)
            return Response(status=status.HTTP_200_OK, data=data)

    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="something went wrong")


@swagger_auto_schema(
    method='get',
    responses={
        200: TSDConfigurationSerializer(),
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='delete',
    responses={
        200: openapi.Response('Configuration object deleted successfully'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Update configuration data',
    ),
    responses={
        200: TSDConfigurationSerializer(),
        400: 'Bad Request - Invalid update data',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET', 'DELETE', 'PATCH'])
@jwt_authenticated
def get_config_object(request, user, tsd_id, pk):
    if request.method == 'GET':
        temp = config_service.get_config(tsd_id, pk, user=user)
        return Response(status=status.HTTP_200_OK, data=temp)

    elif request.method == 'DELETE':
        return Response(status=config_service.delete_config(tsd_id, pk, user))

    elif request.method == "PATCH":
        data = __convert_body(request)
        if validator.validate_tsd_config_builder(data):
            data = config_service.update_config(tsd_id, pk, data, user=user)
            return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of reduced data values'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
@jwt_authenticated
def get_data_reduced_values(request, user, tsd_id, pk):
    data = config_service.get_all_training_data_reduced(tsd_id, pk, user=user)
    return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Preprocessor data',
    ),
    responses={
        200: openapi.Response('Preprocessor handled successfully'),
        400: 'Bad Request - Invalid preprocessor data',
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Update preprocessor data',
    ),
    responses={
        200: openapi.Response('Preprocessor updated successfully'),
        400: 'Bad Request - Invalid update data',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST', 'PATCH'])
@jwt_authenticated
def handle_preprocessor(request, user, tsd_id, pk):
    body = __convert_body(request)
    if request.method == 'POST':
        data = config_service.add_preprocessor(tsd_id, pk, body, user)
        return Response(status=status.HTTP_200_OK, data=data)
    if request.method == 'PATCH':
        data = config_service.add_preprocessor(tsd_id, pk, body, user)
        return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Specific level configuration data',
    ),
    responses={
        200: openapi.Response('Specific level for configuration updated successfully'),
        400: 'Bad Request - Invalid request body',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
@jwt_authenticated
def post_specific_level_for_config(request, user, tsd_id, pk):
    body = __convert_body(request)

    # TODO add specific handling here
    data = config_service.run_model_setup(tsd_id, pk, user=user)
    return Response(status=data, data=data)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Configuration levels data',
    ),
    responses={
        200: openapi.Response('Configuration levels updated successfully'),
        400: 'Bad Request - Invalid request body',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
@jwt_authenticated
def post_config_levels(request, user, tsd_id, pk, td):
    body = __convert_body(request)
    data = config_service.add_level_config_to_configuration(tsd_id, pk, td, user, body)
    return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='post',
    responses={
        200: TSDConfigurationSerializer(),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
@jwt_authenticated
def copy_config(request, user, tsd_id, pk):
    data = config_service.copy_tsd_config(tsd_id, pk, user)
    return Response(status=status.HTTP_200_OK, data=data)


def __convert_body(request):
    return json.loads(request.body.decode("utf-8"))
