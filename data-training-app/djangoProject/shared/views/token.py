from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import JwtUser


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'firstName': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
            'lastName': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name')
        },
        required=['email', 'password', 'firstName', 'lastName'],
    ),
    responses={
        201: openapi.Response('Account created successfully'),
        400: 'Bad Request - User already exists or invalid data'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    password = request.data.get('password')
    email = request.data.get('email')
    email = "django_" + email.lower()
    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')

    # Validation logic here (e.g., check if the user already exists)

    try:
        JwtUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
    except Exception:
        return Response({'detail': 'user already exists'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Account created successfully'}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
        },
        required=['email', 'password'],
    ),
    responses={
        200: openapi.Response('Login successful, token returned'),
        401: 'Unauthorized - Invalid credentials'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = "django_" + request.data.get('email').lower()
    password = request.data.get('password')

    user = JwtUser.objects.filter(email=email).first()

    if user and user.check_password(password):
        print("password match")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'token': access_token}, status=status.HTTP_200_OK)

    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
