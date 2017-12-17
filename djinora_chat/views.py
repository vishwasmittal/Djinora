from django.shortcuts import render
from rest_framework.views import APIView
from djinora_chat.auth_classes import CSRFExemptSessionAuthentication
from djinora_chat.slack_plugin.public_box.serializers import SlackDataSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import get_slack_context


def index(request):
    return render(request, 'djinora_chat/chat.html')


def slack_chat(request):
    return render(request, 'djinora_chat/slack.html')


def register_chat(request):

    context = get_slack_context()
    return render(request, 'djinora_chat/username_entry.html', context=context)


class SlackResponseView(APIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)
    serializer_class = SlackDataSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.validated_data
        return Response(response, status=status.HTTP_200_OK)

