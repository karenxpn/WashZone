from rest_framework import serializers
from assistant.models import Message, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'role', 'content', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True, source='chatmessage_set')

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'messages']
        read_only_fields = ['user']
