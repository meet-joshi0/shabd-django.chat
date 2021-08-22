"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import shabd.routing
import django

from django.core.asgi import get_asgi_application
from channels.routing import get_default_application , ProtocolTypeRouter,URLRouter,ChannelNameRouter
from channels.auth import AuthMiddlewareStack

django.setup()


application =  ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            shabd.routing.websocket_urlpatterns
        )
    )

})
