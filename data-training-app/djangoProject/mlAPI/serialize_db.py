from rest_framework import serializers
from .models import MLModel, MLTrainingInformation, MLConfiguration, MLSolution


class MLModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = '__all__'


class MLTrainingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLTrainingInformation
        fields = '__all__'


class MLConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLConfiguration
        fields = '__all__'


class MLSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLSolution
        fields = ['id', 'ml_configuration']
