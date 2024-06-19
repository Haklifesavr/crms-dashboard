from django.views.generic import TemplateView
from web_project import TemplateLayout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from rest_framework import status
from django.db.models import Q



class ChatView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
    
class ChatSessionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        sessions = ChatSession.objects.filter(
            Q(participant1=request.user) | Q(participant2=request.user)
        )
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     # Logic to create a new chat session if it doesn't exist

class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id, *args, **kwargs):
        try:
            session = ChatSession.objects.get(id=session_id)
            # Ensure the user is part of the chat session
            if request.user == session.participant1 or request.user == session.participant2:
                messages = Message.objects.filter(chat_session=session).order_by('timestamp')
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "You do not have permission to view these messages."}, status=status.HTTP_403_FORBIDDEN)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, session_id, *args, **kwargs):
        session = ChatSession.objects.get(id=session_id)
        # Ensure the user is part of the chat session
        if request.user == session.participant1 or request.user == session.participant2:
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, chat_session=session)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)