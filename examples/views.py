import json
from http import HTTPStatus

import channels.layers
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render


def chat_index(request):
    return render(request, "examples/chat/index.html")


def chat_room(request, room_name):
    return render(request, "examples/chat/room.html", {"room_name": room_name})


def tasks_index(request):
    if request.method != "POST":
        return render(request, "examples/tasks/index.html")

    data = json.loads(request.body.decode("utf-8"))
    message = data.get("message", "Default message")
    channel_layer = channels.layers.get_channel_layer()

    if channel_layer is None:
        return JsonResponse({}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    async_to_sync(channel_layer.send)(
        "background-task-example",
        {
            "type": "message",
            "text": message,
        },
    )

    return JsonResponse({}, status=HTTPStatus.OK)
