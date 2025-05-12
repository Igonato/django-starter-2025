from django.urls import path

from . import views

urlpatterns = [
    path("examples/chat", views.chat_index, name="examples-chat-index"),
    path(
        "examples/chat/<str:room_name>",
        views.chat_room,
        name="examples-chat-room",
    ),
    path("examples/tasks", views.tasks_index, name="examples-tasks-index"),
]
