"""
ASGI config for djangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import django
from django.urls import path
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
application = get_asgi_application()


from shared.consumer import training_consumer
from shared.jwt.jwt_authentication_channel import QueryAuthMiddleware


application = ProtocolTypeRouter({
    "http": application,
    "websocket": QueryAuthMiddleware(
        SessionMiddlewareStack(
            URLRouter([
                path("ws/status/", training_consumer.StatusConsumer.as_asgi()),
            ])
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})
