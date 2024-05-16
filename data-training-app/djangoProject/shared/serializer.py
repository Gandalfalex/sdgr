from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from shared.models import TrainData, JwtUser, PreprocessorType, Preprocessor


class TrainDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainData
        fields = '__all__'


class PreprocessorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreprocessorType
        fields = '__all__'


class PreprocessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preprocessor
        fields = '__all__'


class JwtUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = JwtUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: JwtUser):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        # Add custom claims, if needed
        # token['custom_claim'] = 'custom_value'

        return token

    def validate(self, attrs):
        credentials = {
            'email': attrs['email'],
            'password': attrs['password']
        }
        return super().validate(credentials)


class ImputationAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreprocessorType
        fields = ('name', 'description')
