from rest_framework import serializers
from .models import Board, Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # This serializer is for serializing user information. Adjust fields according to your needs.
    class Meta:
        model = User
        fields = ['username', 'id']  

class StringToIntegerIDField(serializers.Field):
    def to_representation(self, value):
        # For outgoing data, convert integer IDs to strings.
        return str(value)

    def to_internal_value(self, data):
        # For incoming data, convert string IDs back to integers.
        try:
            return int(data)
        except ValueError:
            raise serializers.ValidationError("This field must be an integer or a string that represents an integer.")
        
class ItemSerializer(serializers.ModelSerializer):
    id = StringToIntegerIDField(required=False)
    assigned = UserSerializer(many=True, required=False, allow_null=True)
    members = UserSerializer(many=True, required=False, allow_null=True)
    badge = serializers.CharField(source='badge_color', required=False, allow_null=True)
    # due_date = serializers.DateField(format="%d %B", required=False, allow_null=True)
    due_date = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    
    class Meta:
        model = Item
        fields = ['id', 'title', 'comments', 'badge_text', 'badge', 'due_date', 'attachments', 'assigned', 'members']

class BoardSerializer(serializers.ModelSerializer):
    id = StringToIntegerIDField(required=False)
    item = ItemSerializer(many=True, read_only=True)  

    class Meta:
        model = Board
        fields = ['id', 'title', 'item']

