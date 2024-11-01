# myapp/consumers.py

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        """
        Handles WebSocket connection. Adds the consumer to a WebSocket group and accepts the connection.
        """
        self.group_name = 'user_web'  # Define the group name

        # Add the consumer to the WebSocket group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()  # Accept the WebSocket connection

    def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.
        Removes the consumer from the WebSocket group.
        """
        # Remove the consumer from the WebSocket group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
