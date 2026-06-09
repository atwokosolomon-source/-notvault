# notes/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Note, Subject
from .serializers import NoteSerializer, SubjectSerializer

# ── GET subjects — everyone can see ──────────────────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def get_subjects(request):
    subjects = Subject.objects.all()
    return Response(SubjectSerializer(subjects, many=True).data)

# ── GET notes — everyone / POST — admin only ──────────────────
@api_view(['GET', 'POST'])
def notes_list(request):
    if request.method == 'GET':
        notes = Note.objects.all().order_by('-created_at')
        q = request.GET.get('q', '').strip()
        if q:
            notes = notes.filter(title__icontains=q)
        subject_id = request.GET.get('subject_id')
        if subject_id:
            notes = notes.filter(subject_id=subject_id)
        return Response(NoteSerializer(notes, many=True).data)

    if request.method == 'POST':
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can upload notes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('UPLOAD ERRORS:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ── GET one note / DELETE — admin only ────────────────────────
@api_view(['GET', 'DELETE'])
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'GET':
        return Response(NoteSerializer(note).data)

    if request.method == 'DELETE':
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can delete notes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        note.file.delete(save=False)
        note.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

# ── Download — everyone can download ─────────────────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def note_download(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.downloads += 1
    note.save()
    return FileResponse(
        note.file.open('rb'),
        as_attachment=True,
        filename=note.file.name.split('/')[-1]
    )