from rest_framework import serializers


class CreateMLSolutionSerializer(serializers.Serializer):
    training_data = serializers.ListSerializer(required=True)
