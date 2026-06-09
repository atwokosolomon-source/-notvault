# notes/serializers.py
from rest_framework import serializers
from .models import Note, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Subject
        fields = ['id', 'name', 'color', 'icon']

class NoteSerializer(serializers.ModelSerializer):
    subject_name  = serializers.CharField(source='subject.name',  read_only=True)
    subject_color = serializers.CharField(source='subject.color', read_only=True)

    class Meta:
        model  = Note
        fields = ['id', 'title', 'description', 'subject', 'subject_name',
                  'subject_color', 'file', 'pages', 'downloads', 'author', 'created_at']