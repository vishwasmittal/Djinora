from channels import Channel, Group
from channels.sessions import channel_session

from djinora_chat.models import *
from djinora_chat.utils import message_builder, username_validator

from urllib.parse import parse_qs
import json


@channel_session
def ws_connect(message):
    # accepting the connection
    message.reply_channel.send({'accept': True})
    # parsing the query string
    params = parse_qs(message.content['query_string'].decode())
    # checking for username in query string
    if 'username' in params:
        username = params['username'][0]
        message.channel_session['username'] = username
        message.channel_session['joined'] = False
    else:
        username = None

    keep_alive, outgoing_message = username_validator(username=username)

    if not keep_alive:
        message.reply_channel.send(outgoing_message['reply_message'])
        message.reply_channel.send({'close': True})

    else:
        message.channel_session['joined'] = True
        message.reply_channel.send(outgoing_message['reply_message'])
        Group('public').add(message.reply_channel)
        Group('public').send(outgoing_message['group_message'])

    # validating the username length
    # if len(username) > 36:
    #         message.reply_channel.send({
    #             'text': json.dumps({
    #                 "status": "404",
    #                 "error": "Name too long",
    #                 'state': 'connect',
    #             }),
    #         })
    #         message.reply_channel.send({'close': True})
    #         return
    #     # checking if same username exists
    #     elif TempPublicUser.objects.filter(username=username).count() > 0:
    #         message.reply_channel.send({
    #             'text': json.dumps({
    #                 "status": "409",
    #                 "error": "Username already taken! :(",
    #                 'state': 'connect',
    #             }),
    #         })
    #         message.reply_channel.send({'close': True})
    #         return
    #     elif username == "Slack":
    #         message.reply_channel.send({
    #             'text': json.dumps({
    #                 "status": "403",
    #                 "error": "You are already inside of Slack, <b>Slack</b>!",
    #                 'state': 'connect',
    #             }),
    #         })
    #         message.reply_channel.send({'close': True})
    #         return
    #     # adding username to chat
    #     else:
    #         message.channel_session['joined'] = True
    #         TempPublicUser.objects.create(username=username)
    #         message.reply_channel.send({
    #             'text': json.dumps({
    #                 "status": "200",
    #                 "message": "Welcome to Slack, <b>" + username + "</b>",
    #                 'state': 'connect',
    #                 'username': username,
    #             }),
    #         })
    #         Group('public').add(message.reply_channel)
    #         Group('public').send({
    #             "text": json.dumps({
    #                 "text": "Has joined the channel",
    #                 "username": username,
    #                 "bot": True,
    #                 'state': 'receive',
    #             }),
    #         })
    # closing connection if username not present in request

    # if username not present then send the error message
    # else:
    #     message.reply_channel.send({
    #         'text': json.dumps({
    #             "status": "400",
    #             "text": "Username is required",
    #             'state': 'connect',
    #         }),
    #     })
    #     message.reply_channel.send({'close': True})


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
            'state': 'receive',
        }),
    })


@channel_session
def ws_disconnect(message):
    username = message.channel_session['username']
    Group('public').discard(message.reply_channel)
    if message.channel_session['joined']:
        Group('public').send({
            "text": json.dumps({
                "text": "Has left the chat",
                "username": username,
                "bot": True,
                'state': 'receive',
            }),
        })
