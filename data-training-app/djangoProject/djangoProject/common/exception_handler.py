import logging

from django.http import JsonResponse
from rest_framework import status

from djangoProject.common.default_exceptions.bad_request_exception import BadRequestException
from djangoProject.common.default_exceptions.invalid_file_type_exception import InvalidFileTypeException
from djangoProject.common.default_exceptions.not_found_exception import NotFoundException
from rest_framework.views import exception_handler as drf_exception_handler

from djangoProject.common.default_exceptions.unique_constraint_violation_exception import \
    UniqueConstraintViolationException
from djangoProject.common.default_exceptions.unknown_error_exception import UnknownErrorException
from djangoProject.common.default_exceptions.user_not_authenticated import UserNotAuthenticated


def exception_handler(exc, context):
    """
    Custom exception handler for Django REST framework.
    """

    def build_error_response(exception, status_code):
        response_data = {
            "error": str(exception),
            "reason": exception.reason if hasattr(exception, 'reason') else None,
            "i18nKey": exception.i18nKey if hasattr(exception, 'i18nKey') else "UNDEFINED"
        }
        return JsonResponse(response_data, status=status_code)

    exception_mapping = {
        NotFoundException: status.HTTP_404_NOT_FOUND,
        BadRequestException: status.HTTP_400_BAD_REQUEST,
        InvalidFileTypeException: status.HTTP_400_BAD_REQUEST,
        UnknownErrorException: status.HTTP_500_INTERNAL_SERVER_ERROR,
        UniqueConstraintViolationException: status.HTTP_409_CONFLICT,
        UserNotAuthenticated: status.HTTP_403_FORBIDDEN
    }

    if type(exc) in exception_mapping:
        return build_error_response(exc, exception_mapping[type(exc)])

    if isinstance(exc, UnknownErrorException):
        logging.error(f"unknown error: {exc}")

    response = drf_exception_handler(exc, context)
    if response is not None:
        return response

    return JsonResponse({'error': 'Unexpected server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
