import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from shared.jwt.jwt_authenticate import jwt_authenticated
from shared.models import Survey

@swagger_auto_schema(
    method='post',
    responses={
        200: 'Survey submitted successfully',
        400: 'Bad Request - Empty request body or invalid JSON document',
        500: 'Internal Server Error - Something went wrong'
    }
)
@api_view(['POST'])
@jwt_authenticated
def post_survey(request, user):
    if request.body is None:
        raise BadRequestException("empty request body", "this method expects a json document")
    try:
        req_body = json.loads(request.body.decode("utf-8"))
        element = Survey.objects.filter(user=user).first()
        if element is not None:
            element.result = req_body
        else:
            element = Survey(user=user, result=req_body)
        element.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        raise UnknownErrorException("something went wrong",str(e))
