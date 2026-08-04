from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from .models import Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.username = self.scope["url_route"]["kwargs"]["username"]

        async_to_sync(self.channel_layer.group_add)(
            self.username,
            self.channel_name
        )

        self.accept()

        print(self.username, "Connected")


    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.username,
            self.channel_name
        )

        print(self.username, "Disconnected")


    def receive(self, text_data):
        data = json.loads(text_data)

        sender = self.username
        receiver = data["receiver"]
        message = data["message"]

        print("Sender :", sender)
        print("Receiver :", receiver)
        print("Message :", message)

         # Persist the message so it survives a page refresh.
        Message.objects.create(sender=sender, receiver=receiver, message=message)

        async_to_sync(self.channel_layer.group_send)(
            receiver,
            {
                "type": "chat_message",
                "sender": sender,
                "message": message
            }
        )

        # Also echo the message back to the sender's own group so it
        # shows up in their own chatbox (skip if chatting with yourself,
        # to avoid receiving the same message twice).
        if receiver != sender:
            async_to_sync(self.channel_layer.group_send)(
                sender,
                {
                    "type": "chat_message",
                    "sender": sender,
                    "message": message
                }
            )

    # Handles events with "type": "chat_message" sent via group_send.
    # Channels dispatches group_send events by calling the method whose
    # name matches the "type" value, so this method is required.
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "sender": event["sender"],
            "message": event["message"]
        }))