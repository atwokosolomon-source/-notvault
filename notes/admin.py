# notes/admin.py
from django.contrib import admin
from .models import Subject, Note

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'icon']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'subject', 'author', 'downloads', 'created_at']
    list_filter   = ['subject']
    search_fields = ['title', 'author']