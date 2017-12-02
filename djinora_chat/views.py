from django.shortcuts import render


def index(request):
    return render(request, 'djinora_chat/chat.html')


def slack_chat(request):
    return render(request, 'djinora_chat/slack.html')
