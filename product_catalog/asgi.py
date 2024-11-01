"""
ASGI config for jsbpayroll project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter ##new
import products.routing
import products
import django 
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_catalog.settings')
django.setup() 
asgi_application = get_asgi_application()
application = ProtocolTypeRouter({
	'http': asgi_application,
	'websocket':
	AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(users.routing.websocket_urlpatterns)
		),
	)
})


