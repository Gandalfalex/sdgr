import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from mlAPI.service.simulation_service import load_solution_from_trained_model, forecast_data_from_trained_model
from shared.jwt.jwt_authenticate import jwt_authenticated


@swagger_auto_schema(
    method='post',
    responses={
        200: openapi.Response('Configuration loaded successfully'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
@jwt_authenticated
def load_config(request, user, m_id, pk):
    result = load_solution_from_trained_model(user, m_id, pk)
    return Response(status=status.HTTP_200_OK, data=result)


@api_view(['POST'])
@jwt_authenticated
def forecast_config(request, user, m_id, pk):
    if request.body is None:
        raise BadRequestException("empty request body", "this method expects a json document")
    try:
        req_body = json.loads(request.body.decode("utf-8"))
        data = forecast_data_from_trained_model(req_body, user, m_id, pk)
        return Response(status=status.HTTP_200_OK, data=data)
    except Exception as e:
        raise UnknownErrorException("something went wrong", str(e))
