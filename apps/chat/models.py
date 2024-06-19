from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    participant1 = models.ForeignKey(User, related_name='chat_sessions_as_participant1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(User, related_name='chat_sessions_as_participant2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant1.username} and {self.participant2.username}"

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='authored_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.author.username} at {self.timestamp}"
