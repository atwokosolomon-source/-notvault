# notes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('subjects/',                views.get_subjects),
    path('notes/',                   views.notes_list),
    path('notes/<int:pk>/',          views.note_detail),
    path('notes/<int:pk>/download/', views.note_download),
]