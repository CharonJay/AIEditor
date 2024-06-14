from django.contrib import admin
from django.urls import path
from .views import ChatView

from chat import views

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat")

]
