import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from mlAPI import validator
from mlAPI.service.solution_builder_service import SolutionBuilderService
from shared.jwt.jwt_authenticate import jwt_authenticated
from shared.services.preprocessor_service import get_preprocessor_for_from_ml

solution_service = SolutionBuilderService()


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of configurations'),
        500: 'Internal Server Error - Something went wrong'
    }
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='JSON document for creating a configuration',
    ),
    responses={
        200: openapi.Response('Configuration created successfully'),
        400: 'Bad Request - Invalid request body or JSON document',
        500: 'Internal Server Error - Something went wrong'
    }
)
@api_view(['POST', 'GET'])
@jwt_authenticated
def configuration_view(request, user, m_id):
    if request.method == 'GET':
        data = solution_service.get_configurations(m_id, user=user)
        return Response(status=status.HTTP_200_OK, data=data)

    elif request.method == 'POST':
        if request.body is None:
            raise BadRequestException("empty request body", "this method expects a json document")
        try:
            req = json.loads(request.body.decode("utf-8"))
            print(req)
        except Exception as e:
            logging.info(f"could not decode request {e}")
            raise BadRequestException("could not decode request body", str(e))

        if validator.validate_ml_solution_builder(req):
            data = solution_service.create_configuration(req, m_id, user=user)
            return Response(status=status.HTTP_200_OK, data=data)

    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="something went wrong")


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of solution object'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='delete',
    responses={
        200: openapi.Response('Solution object deleted successfully'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='JSON document for updating a solution object',
    ),
    responses={
        200: openapi.Response('Solution object updated successfully'),
        400: 'Bad Request - Invalid JSON document',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET', 'DELETE', 'PATCH'])
@jwt_authenticated
def get_solution_object(request, user, m_id, pk):
    if request.method == 'GET':
        data = solution_service.get_configuration(m_id, pk, user=user)
        return Response(status=status.HTTP_200_OK, data=data)

    elif request.method == 'DELETE':
        return Response(status=solution_service.delete_configuration(m_id, pk, user))

    elif request.method == "PATCH":
        data = json.loads(request.body.decode("utf-8"))
        if validator.validate_ml_solution_builder(data):
            data = solution_service.update_configuration(data, m_id, pk, user=user)
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
def get_data_reduced_values(request, user, m_id, pk):
    data = solution_service.get_all_training_data_reduced(m_id, pk, user=user)
    return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of preprocessor data'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@swagger_auto_schema(
    method='delete',
    responses={
        501: 'Not Implemented'
    }
)
@swagger_auto_schema(
    method='patch',
    responses={
        501: 'Not Implemented'
    }
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='JSON document for adding a preprocessor',
    ),
    responses={
        200: openapi.Response('Preprocessor added successfully'),
        400: 'Bad Request - Invalid JSON document',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET', 'DELETE', 'PATCH', 'POST'])
@jwt_authenticated
def handle_preprocessor(request, user, m_id, pk):
    if request.method == 'GET':
        data = get_preprocessor_for_from_ml(m_id, pk, user)
        return Response(status=status.HTTP_200_OK, data=data)
    elif request.method == 'DELETE':
        return Response(status=501)
    elif request.method == 'PATCH':
        return Response(status=501)
    elif request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        data = solution_service.add_preprocessor_to_configuration(m_id, pk, body, user)
        return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='post',
    responses={
        200: openapi.Response('Solution copied successfully'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
@jwt_authenticated
def copy_solution(request, user, m_id, pk):
    data = solution_service.copy_ml_solution(m_id, pk, user=user)
    return Response(status=status.HTTP_200_OK, data=data)
