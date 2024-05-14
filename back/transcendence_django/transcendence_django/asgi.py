import os
from back_game.app_settings.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transcendence_django.settings")

application = ProtocolTypeRouter(
	{
		"http": get_asgi_application(),
		"websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
	}
)
