from rest_framework import serializers

from .models import Entry, User

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'name', 'description', 'completed', 'parentId', 'type', 'difficulty']

class UserSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'auth0Id', 'level', 'xp', 'entries']
