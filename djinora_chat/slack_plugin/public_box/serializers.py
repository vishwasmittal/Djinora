from rest_framework import serializers
from channels import Group
from djinora_chat.utils import message_builder  # , send_message
from djinora_chat.models import *
from djinora_chat.slack_plugin.slack_team_info import users_list


class SlackEventSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    user = serializers.CharField(max_length=9, required=False)
    channel = serializers.CharField(max_length=9, required=False)
    text = serializers.CharField(required=False)


class SlackDataSerializer(serializers.Serializer):
    event_time = serializers.IntegerField(required=False)
    event = SlackEventSerializer(required=False)
    challenge = serializers.CharField(required=False)
    response = serializers.CharField(required=False, read_only=True)

    class Meta:
        fields = ('event', 'challenge', 'response', 'event_time')

    def create(self, validated_data):
        if 'challenge' in validated_data:
            self.validated_data['response'] = validated_data.get('challenge')
            return self.validated_data['response']
        event_time = validated_data.get('event_time')
        event = validated_data.get('event')
        if 'user' not in event:     # will not process if its from bot (this can be when public users send message)
            return ""
        user = event.get('user')
        user_object = SlackUser.objects.filter(uid=user)
        if user_object.count() == 0:
            users_list()
            user_object = SlackUser.objects.filter(uid=user)
        channel = event.get('channel')
        type = event.get('type')
        if 'text' in event:
            text = event.get('text')
            group_message = message_builder(state='r', status=200, message=text, bot=False,
                                            username=user_object[0].first_name())
            Group('public').send(group_message)
            # response = send_message(user_input=text, user=user, channel=channel, text=text)
            response = group_message
        else:
            text = None
            response = {}
        self.validated_data['response'] = response
        return response

    def update(self, instance, validated_data):
        return None


