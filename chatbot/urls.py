from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path("api/chat/", chatbot_view, name="chatbot"),
]

