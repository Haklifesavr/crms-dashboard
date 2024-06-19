# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# from .models import ChatRoom, Message  # Import both models

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']  # Get authenticated user
#         self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']

#         try:
#             self.chat_room = ChatRoom.objects.get(pk=self.chat_room_id)
#             if self.user not in self.chat_room.users.all():
#                 return self.close(code=403)  # Close if not a member
#         except ChatRoom.DoesNotExist:
#             return self.close(code=404)  # Close if chat room doesn't exist

#         self.room_group_name = f'chat_{self.chat_room.id}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

        

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = self.user.username  # Use username instead of sender field

#         # Save message to database (optional)
#         await self.save_message(sender, message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender
#         }))

#     async def save_message(self, sender, message):
#         """Saves a chat message to the database."""

#         new_message = Message.objects.create(
#             chat_room=self.chat_room,
#             sender=self.user,
#             content=message,
#         )

#         # Additional logic (optional)
#         #  - Handle potential errors during saving
#         #  - Broadcast a message about the save operation (if needed)
