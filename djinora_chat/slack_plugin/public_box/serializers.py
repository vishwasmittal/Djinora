from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate


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
        user = event.get('user')
        channel = event.get('channel')
        type = event.get('type')
        if 'text' in event:
            text = event.get('text')
        else:
            text = None
        # response = send_message(user_input=text, user=user, channel=channel, event_time=event_time)
        # self.validated_data['response'] = response
        # return response
        return ""

    def update(self, instance, validated_data):
        return None
