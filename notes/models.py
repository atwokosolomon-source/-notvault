# notes/models.py
from django.db import models

class Subject(models.Model):
    name  = models.CharField(max_length=80)
    color = models.CharField(max_length=20, default='#7a7a95')
    icon  = models.CharField(max_length=10, default='📚')

    def __str__(self):
        return self.name

class Note(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject     = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    file        = models.FileField(upload_to='pdfs/')   # Django handles storage
    pages       = models.IntegerField(default=0)
    downloads   = models.IntegerField(default=0)
    author      = models.CharField(max_length=100, default='Anonymous')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title