from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mlAPI.models import MLTrainingInformation
from mlAPI.serialize_db import MLTrainingInformationSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: MLTrainingInformationSerializer(),
        204: 'No Content - Could not find the solution',
        500: 'Internal Server Error - Unexpected error'
    }
)
@api_view(['GET'])
def get_information_by_config_id(request, m_id, c_id):
    try:
        information = MLTrainingInformation.objects.get(ml_solution=c_id)
        serializer = MLTrainingInformationSerializer(information)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    except MLTrainingInformation.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT, data={"could not find solution"})
