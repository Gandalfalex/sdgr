from tokenize import TokenError

from channels.db import database_sync_to_async
from jwcrypto import jwt, jwk
from jwcrypto.common import json_decode
from jwcrypto.jws import InvalidJWSSignature
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken
from urllib.parse import parse_qs
from djangoProject import settings


@database_sync_to_async
def get_user(token):
    try:
        key = jwk.JWK(kty='oct', k=settings.SECRET_KEY)
        try:
            jws_token = jwt.JWT(key=key, jwt=token)
            payload = json_decode(jws_token.claims)
            if 'sub' not in payload or 'iat' not in payload or 'exp' not in payload:
                raise InvalidToken("Token has invalid payload")

            user = authentication.get_user_model().objects.get(email=payload['sub'])
            return user

        except InvalidJWSSignature:
            raise ValueError("Invalid token signature")
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")
    except TokenError as e:
        raise InvalidToken(str(e))


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict["token"][0]

        scope["ml_id"] = query_dict["ml_id"][0]
        scope["sol_id"] = query_dict["sol_id"][0]

        scope["user"] = await get_user(token)
        return await self.app(scope, receive, send)
