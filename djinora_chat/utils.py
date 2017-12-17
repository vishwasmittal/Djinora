from djinora_chat.slack_plugin import slack_team_info
from djinora_chat import serializers


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




