from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import shared.services.preprocessor_service as ps


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of preprocessor types'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def get_all_preprocessor_types(res):
    data = ps.get_all_preprocessor_types()
    return Response(status=status.HTTP_200_OK, data=data)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('Successful retrieval of the specified preprocessor type'),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def get_preprocessor_type(res, type_id):
    data = ps.get_preprocessor_type(type_id)
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(['POST'])
def save_all_preprocessor_types(res):
    pass
