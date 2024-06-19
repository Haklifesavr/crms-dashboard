from django.urls import path
from .views import ChatSessionListCreateView, MessageCreateView, ChatView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/chats/",
        login_required(ChatView.as_view(template_name="app_chat.html")),
        name="app-chat",
    ),
    path('chats/', ChatSessionListCreateView.as_view(), name='chat_sessions'),
    path('chats/<int:session_id>/messages/', MessageCreateView.as_view(), name='send_message'),
]
