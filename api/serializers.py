from rest_framework import serializers

from .models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'name', 'description', 'completed', 'parentId', 'type', 'difficulty']