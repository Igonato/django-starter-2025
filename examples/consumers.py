import json

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from django.db.utils import ImproperlyConfigured


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.channel_layer is None:
            raise ImproperlyConfigured("CHANNEL_LAYER must be configured")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        if self.channel_layer is None:
            raise ImproperlyConfigured("CHANNEL_LAYER must be configured")

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if self.channel_layer is None:
            raise ImproperlyConfigured("CHANNEL_LAYER must be configured")

        if text_data is None:
            return

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


class BackgroundTaskConsumer(SyncConsumer):
    def message(self, message):
        print("Recieved message: " + message["text"])
