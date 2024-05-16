import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shared.jwt.jwt_authenticate import jwt_authenticated
from tsaAPI.services.tsd_config_service import TsdConfigService

config_service = TsdConfigService()


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of configuration graph'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='Configuration graph request data',
    ),
    responses={
        200: openapi.Response('Configuration graph created successfully'),
        400: 'Bad Request - Invalid request body',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET', 'POST'])
@jwt_authenticated
def get_configuration_graph(request, user, tsd_id, pk):
    if request.method == 'POST':
        body = __convert_body(request)
        data = config_service.run_model_setup_with_custom_body(tsd_id, pk, body, user=user)
        return Response(status=status.HTTP_200_OK, data={"data": data})
    if request.method == 'GET':
        data = config_service.run_model_setup(tsd_id, pk, user=user)
        return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of configuration graph for training data'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
@jwt_authenticated
def get_configuration_graph_for_train_data(request, user, tsd_id, pk, td):
    data = config_service.run_model_single_data(tsd_id, pk, td, user=user)
    return Response(status=status.HTTP_200_OK, data=data)


def __convert_body(request):
    return json.loads(request.body.decode("utf-8"))
