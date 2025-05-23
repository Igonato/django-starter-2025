from django.urls import re_path

from . import consumers

urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

name_routes = {
    "background-task-example": consumers.BackgroundTaskConsumer.as_asgi(),
}
