from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def jwt_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_403_FORBIDDEN)
        return view_func(request, request.user, *args, **kwargs)

    return _wrapped_view
