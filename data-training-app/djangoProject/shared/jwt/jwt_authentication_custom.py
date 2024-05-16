from django.http import HttpRequest
from jwcrypto import jwt, jwk
from jwcrypto.common import json_decode
from jwcrypto.jws import InvalidJWSSignature

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import authentication

from djangoProject import settings
import threading

from djangoProject.common.default_exceptions.user_not_authenticated import UserNotAuthenticated

_request_local = threading.local()


class BypassJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None
        validated_token = self.validate_token(header)
        if 'sub' not in validated_token or 'iat' not in validated_token or 'exp' not in validated_token:
            raise InvalidToken("Token has invalid payload")

        user = authentication.get_user_model().objects.get(email=validated_token['sub'])
        _request_local.user = user

        if hasattr(_request_local, 'user'):
            del _request_local.user

        return user, raw_token

    def validate_token(self, token):
        try:
            raw_token = str(token).split(" ")[1][:-1]
            key = jwk.JWK(kty='oct', k=settings.SECRET_KEY)
            try:
                jws_token = jwt.JWT(key=key, jwt=raw_token)
                payload = json_decode(jws_token.claims)
                return payload

            except InvalidJWSSignature:
                raise UserNotAuthenticated("Invalid token signature", "provide a valid token")
            except Exception as e:
                raise UserNotAuthenticated(f"Invalid token: {str(e)}", "login again")
        except TokenError as e:
            raise InvalidToken(str(e))
