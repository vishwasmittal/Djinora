from djinora_chat.slack_plugin import slack_team_info
from djinora_chat import serializers
from djinora_chat.models import *
import json


def get_slack_context():
    public_channel_info = slack_team_info.public_channel_info()
    users_online = slack_team_info.active_public_users()
    team_info = slack_team_info.team_info()
    if team_info is not None or users_online is not None or public_channel_info is not None:
        context = {
            'team_name': team_info['name'],
            'team_logo': team_info['logo'],
            'team_domain': team_info['domain'],
            'users_online': users_online,
            'channel_name': public_channel_info['name'],
            'channel_members': public_channel_info['members'],
            'channels_num_members': public_channel_info['num_members'],
            'channel_id': public_channel_info['id'],
        }
    else:
        # return default context
        context = {
            'team_name': "Awesome Team",
            'team_logo': None,
            'team_domain': 'awesome_team',
            'users_online': [],
            'channel_name': 'public',
            'channel_members': [],
            'channels_num_members': 0,
            'channel_id': 'C00PUBLIC',
        }
    return context


def username_validator(username):
    """ checks if username is valid and available and if yes
    signals the consumer to accept the user and also provides
    the message to be sent to user and group
    """

    # else:
    #     message.reply_channel.send({
    #         'text': json.dumps({
    #             "status": "400",
    #             "text": "Username is required",
    #             'state': 'connect',
    #         }),
    #     })
    #     message.reply_channel.send({'close': True})

    if username is None:
        error = 'Username is required'
        reply_message = message_builder(state='c', status=404, message=error, username=username)
        return False, {
            'bool_reply': True,
            'bool_group': False,
            'reply_message': reply_message,
        }

    elif len(username) > 36:
        # message.reply_channel.send({
        #     'text': json.dumps({
        #         "status": "404",
        #         "error": "Name too long",
        #         'state': 'connect',
        #     }),
        # })
        error = 'Name to long'
        reply_message = message_builder(state='c', status=404, message=error, username=username)
        # message.reply_channel.send({'close': True})
        return False, {
            'bool_reply': True,
            'bool_group': False,
            'reply_message': reply_message,
        }

        # checking if same username exists
    elif TempPublicUser.objects.filter(username=username).count() > 0:
        # message.reply_channel.send({
        #     'text': json.dumps({
        #         "status": "409",
        #         "error": "Username already taken! :(",
        #         'state': 'connect',
        #     }),
        # })
        error = 'Username already taken! :('
        reply_message = message_builder(state='c', status=404, message=error, username=username)
        # message.reply_channel.send({'close': True})
        return False, {
            'bool_reply': True,
            'bool_group': False,
            'reply_message': reply_message,
        }

    # if the username entered is 'Slack'
    elif username == "Slack":
        # message.reply_channel.send({
        #     'text': json.dumps({
        #         "status": "403",
        #         "error": "You are already inside of Slack, <b>Slack</b>!",
        #         'state': 'connect',
        #     }),
        # })
        error = 'You are already inside of Slack, <b>Slack</b>!'
        reply_message = message_builder(state='c', status=404, message=error, username=username)
        # message.reply_channel.send({'close': True})
        return False, {
            'bool_reply': True,
            'bool_group': False,
            'reply_message': reply_message,
        }

    # adding username to chat
    else:
        # message.channel_session['joined'] = True
        TempPublicUser.objects.create(username=username)
        # message.reply_channel.send({
        #     'text': json.dumps({
        #         "status": "200",
        #         "message": "Welcome to Slack, <b>" + username + "</b>",
        #         'state': 'connect',
        #         'username': username,
        #     }),
        # })

        message = "Welcome to Slack, <b>" + username + "</b>"
        reply_message = message_builder(state='c', status=200, message=message, username=username)
        # Group('public').add(message.reply_channel)
        # Group('public').send({
        #     "text": json.dumps({
        #         "text": "Has joined the channel",
        #         "username": username,
        #         "bot": True,
        #         'state': 'receive',
        #     }),
        # })
        message = 'Has joined the channel'
        group_message = message_builder(state='c', status=200, message=message, username=username, bot=True)

        return True, {
            'bool_reply': True,
            'bool_group': True,
            'reply_message': reply_message,
            'group_message': group_message,
        }


def message_builder(state, status, username, message, bot=False):
    serialized_message = serializers.MessageSerializer(data={
        'state': state,
        'status': status,
        'message': message,
        'username': username,
        'bot': bot,
    })

    if serialized_message.is_valid():
        pass
    else:
        # specify that there is a server error
        serialized_message = serializers.MessageSerializer(data={
            'state': 'r',
            'status': 500,
            'message': "Internal Server Error",
            'username': "SysAdmin",
        })

    return serialized_message
