from django.contrib import admin
from django.urls import path
from .views import ChatView, ImageGeneratorView

from chat import views

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path('getsummary/', views.AI_summary, name='getsummary'),
    path('getpolish/', views.AI_polish, name='getpolish'),
    path('getcontinuation/', views.AI_continuation, name='getcontinuation'),
    path('getcorrection/', views.AI_correction, name='getcorrection'),
    path('gettranslation/', views.AI_translation, name='gettranslation'),
    path('upload/', views.handle_upload, name='upload'),
    path('ocr/', views.AI_ocr, name='ocr'),
    path('asr/', views.AI_asr, name='asr'),
    path('delatemultifile/', views.delete_multi_file, name='delatemultifile'),
    path('format/',views.AI_Format, name='format'),
    path('mindmap/', views.AI_mind_map, name='mindmap'),
    path('generate-image/', ImageGeneratorView.as_view(), name='generate_image'),
]
