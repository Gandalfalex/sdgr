import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from mlAPI.models import *
from mlAPI.serialize_db import MLModelsSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: MLModelsSerializer(many=True),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def mlmodels_list(request):
    if request.method == 'GET':
        mlmodels = MLModel.objects.all()
        serializer = MLModelsSerializer(mlmodels, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        200: MLModelsSerializer(),
        204: 'No Content - ML model not found',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def mlmodels_detail(request, pk):
    try:
        mlmodel = MLModel.objects.get(pk=pk)
    except MLModel.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        serializer = MLModelsSerializer(mlmodel)
        return Response(serializer.data)


@api_view(['POST'])
@swagger_auto_schema(
    method='post',
    request_body=MLModelsSerializer,
    responses={
        201: MLModelsSerializer(),
        400: 'Bad Request - Invalid data',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['POST'])
def post_new_model(request):
    try:
        data = JSONParser().parse(request)
        serializer = MLModelsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

    except Exception as e:
        logging.error(f'error {str(e)}')
        return Response(data={'error': str(e)}, status=400)
