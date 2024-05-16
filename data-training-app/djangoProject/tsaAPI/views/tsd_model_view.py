from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tsaAPI.models import TSDModel
from tsaAPI.serialize_db import TSDModelSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: TSDModelSerializer(many=True),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def tsd_models_list(request):
    if request.method == 'GET':
        mlmodels = TSDModel.objects.all()
        serializer = TSDModelSerializer(mlmodels, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        200: TSDModelSerializer(),
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def tsd_models_by_id(request, tsd_id):
    if request.method == 'GET':
        mlmodels = TSDModel.objects.get(pk=tsd_id)
        serializer = TSDModelSerializer(mlmodels)
        return Response(serializer.data)
