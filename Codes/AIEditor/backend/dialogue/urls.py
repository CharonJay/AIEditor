from django.contrib import admin
from django.urls import path
from .views import ChatView

from dialogue import views

urlpatterns = [
    path("dialogue/<int:user_id>/", ChatView.as_view(), name="chat"),
    path("getKB/<int:user_id>/", views.get_kb, name='get_kb'),
    path("addNewPDF/<int:user_id>/", views.add_new_pdf, name='addNewPDF'),
    path("addNewStr/<int:user_id>/", views.add_new_str, name='addNewStr'),
    path("deleteDocument/<int:user_id>/", views.de_document, name='deleteDocument'),
    path("getDocument/<int:user_id>/", views.get_document, name='getDocument'),
    path("kbChat/<int:user_id>/", views.kb_chat, name='kbChat')
]
