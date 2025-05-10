from django.urls import path

from . import views

urlpatterns = [
    path("examples/chat", views.chat_index, name="chat-index"),
    path("examples/chat/<str:room_name>", views.chat_room, name="chat-room"),
]
