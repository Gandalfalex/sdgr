from rest_framework import serializers

from shared.models import TrainData
from tsaAPI.models import TSDConfiguration, TSDTrainingInformation, TSDModel


class TSDModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSDModel
        fields = "__all__"


class TSDTrainingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSDTrainingInformation
        fields = "__all__"


class TSDConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSDConfiguration
        fields = "__all__"


class TrainDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainData
        fields = "__all__"

