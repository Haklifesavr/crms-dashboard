from django.contrib import admin
from .models import ChatSession, Message

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant1', 'participant2', 'created_at')
    search_fields = ('participant1__username', 'participant2__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_session', 'author', 'timestamp', 'short_content')
    search_fields = ('author__username', 'content')
    list_filter = ('timestamp', 'author')

    def short_content(self, obj):
        return obj.content[:50]  # Truncate content after 50 characters
