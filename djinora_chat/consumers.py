from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session

import json


@channel_session
def ws_connect(message):
    if 'username' in message.content['text']:
        message.reply_channel.send({'accept': True})
        username = message.content['text']['username']
        message.channel_session['username'] = username
        Group('public').add(message.reply_channel)
        username = message.channel_session['username']
        Group('public').discard(message.reply_channel)
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
