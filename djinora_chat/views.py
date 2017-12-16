from django.shortcuts import render

from .utils import get_slack_context


def index(request):
    return render(request, 'djinora_chat/chat.html')


def slack_chat(request):
    return render(request, 'djinora_chat/slack.html')


def register_chat(request):

    context = get_slack_context()

    return render(request, 'djinora_chat/username_entry.html', context=context)
