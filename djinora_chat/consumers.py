from channels import Channel, Group
from channels.sessions import channel_session

from urllib.parse import parse_qs
import json


@channel_session
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    params = parse_qs(message.content['query_string'].decode())
    if 'username' in params:
        username = params['username'][0]
        message.channel_session['username'] = username
        Group('public').add(message.reply_channel)
        Group('public').send({
            "text": json.dumps({
                "text": "has joined the channel",
                "username": username,
                "bot": True,
            }),
        })
    else:
        message.reply_channel.send({'close': True})


@channel_session
def ws_receive(message):
    if 'username' not in message.channel_session:
        message.reply_channel.disconnect(message)
    sender = message.channel_session['username']
    Group('public').send({
        "text": json.dumps({
            "username": sender,
            "text": message.content['text'],
            "bot": False,
        }),
    })


@channel_session
def ws_disconnect(message):
    username = message.channel_session['username']
    Group('public').discard(message.reply_channel)
    Group('public').send({
        "text": json.dumps({
            "text": "has left the chat",
            "username": username,
            "bot": True,
        }),
    })
