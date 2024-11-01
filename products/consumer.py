# myapp/consumers.py

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        """
        Handles WebSocket connection.
        Retrieves jsbaccountid and username from query parameters,
        adds the consumer to a WebSocket group, and accepts the connection.
        """

        if self.jsbaccountid:
            self.group_name = f"user_web"
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()

           
        else:
            self.close(code=4403)  # Custom code for unauthorized access


    def disconnect(self, close_code=4403):
        """
        Handles WebSocket disconnection.
        Removes the consumer from WebSocket group and updates active users cache.
        """
        if self.jsbaccountid and self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )
            
           
    
    

    
    
    

