from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from celery_progress.websockets import routing
from notifications_app.routing import websocket_urlpatterns

# Initialize Django ASGI application first
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
    # WebSocket handler for Channels
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.urlpatterns +
            websocket_urlpatterns
        )
    ),
})
