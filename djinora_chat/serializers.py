from rest_framework import serializers

STATE_CHOICE = [
    ('c', 'connect'),
    ('r', 'receive'),
]

STATUS_CHOICES = [
    200,
    400,
    403,
    404,
    409,
    500,
]


class MessageSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=STATE_CHOICE)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    username = serializers.CharField(max_length=36)
    message = serializers.CharField()
    bot = serializers.BooleanField(default=False)


class MessageWrapperSerializer(serializers.Serializer):
    text = MessageSerializer()


msg_ser = MessageSerializer(data={
    'state': 'c',
    'status': '200',
    'username': "custom_username",
    'message': 'custom message',
})

# msg_ser = MessageSerializer()


print(msg_ser.is_valid())

print(msg_ser.data)

