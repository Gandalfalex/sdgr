from rest_framework import viewsets

from tsaAPI.models import TSDTrainingInformation
from tsaAPI.serialize_db import TSDTrainingInformationSerializer


class TSDTrainingInformationViewSet(viewsets.ModelViewSet):
    queryset = TSDTrainingInformation.objects.all()
    serializer_class = TSDTrainingInformationSerializer

