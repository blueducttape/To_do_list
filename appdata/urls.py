from django.urls import path

from .views import NoteView, NoteDetailView, NoteEditorView

app_name = "to_do_list"
urlpatterns = [
    path('notes/', NoteView.as_view(), name='notes'),
    path('notes/<int:note_id>/', NoteDetailView.as_view(), name='note'),
    path('notes/add/', NoteEditorView.as_view(), name='add'),
    path('notes/<int:note_id>/save/', NoteEditorView.as_view(), name='save'),
]