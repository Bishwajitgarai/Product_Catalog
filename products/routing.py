# myapp/routing.py
from django.urls import re_path,path
from consumer import NotificationConsumer
websocket_urlpatterns = [
    path("ws/users/web/", NotificationConsumer.as_asgi()),
]
