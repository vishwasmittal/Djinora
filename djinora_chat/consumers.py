from channels import Channel, Group
from channels.sessions import channel_session

from djinora_chat.utils import message_builder, username_validator

from urllib.parse import parse_qs


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


@channel_session
def ws_receive(message):
    if 'username' not in message.channel_session:
        message.reply_channel.disconnect(message)
    sender = message.channel_session['username']
    group_message = message_builder(state='r', status='200', message=message.content['text'], bot=False, username=sender)
    Group('public').send(group_message)


@channel_session
def ws_disconnect(message):
    username = message.channel_session['username']
    Group('public').discard(message.reply_channel)
    if message.channel_session['joined']:
        group_message = message_builder(state='r', status='200', message='Has left the chat', bot=True, username=username)
        Group('public').send(group_message)

