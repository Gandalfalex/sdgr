from rest_framework.exceptions import PermissionDenied


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            'admin',
            'swagger',
            'redoc'
            'ws/status/',
            'metrics',
            'metrics/extended'
        ]

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        if not any([exempt_url for exempt_url in self.exempt_urls if path.startswith(exempt_url)]):
            header = request.headers.get('Authorization')
            if not header or "Bearer" not in header:
                raise PermissionDenied("JWT token is missing or not in the correct format")

        response = self.get_response(request)
        return response
