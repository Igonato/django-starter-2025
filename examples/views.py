from django.shortcuts import render


def chat_index(request):
    return render(request, "examples/chat/index.html")


def chat_room(request, room_name):
    return render(request, "examples/chat/room.html", {"room_name": room_name})
