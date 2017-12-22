import os
import json
from slackclient import SlackClient
from djinora_chat.models import SlackUser
from djinora_chat import utils


BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(BOT_TOKEN)


def raw_team_info():
    return slack_client.api_call('team.info')


def team_info():
    # return the info of the team, name, logo
    raw_data = raw_team_info()
    if not raw_data['ok']:
        return None
    else:
        return {
            'name': raw_data['team']['name'],
            'logo': raw_data['team']['icon']['image_44'],
            'domain': raw_data['team']['domain'],
        }


def raw_channels_list():
    return slack_client.api_call('channels.list')


def channels_list():
    # returns the list of channels
    raw_data = raw_channels_list()
    if not raw_data['ok']:
        return None
    else:
        return raw_data['channels']


def raw_channel_info(channel=None):
    return slack_client.api_call('channels.info', channel=channel)


def public_channel_info(public_channel_name='public'):
    # return all the info about public channel
    all_channels_list = channels_list()
    if all_channels_list is None:
        return None
    raw_public_channel = None
    for channel in all_channels_list:
        if channel['name'] == public_channel_name:
            raw_public_channel = channel
            break

    if raw_public_channel is None:
        return None

    return {
        'name': raw_public_channel['name'],
        'id': raw_public_channel['id'],
        'num_members': raw_public_channel['num_members'],
        'members': raw_public_channel['members'],
    }


def raw_users_list():
    return slack_client.api_call('users.list', presence=True)


def update_slack_members(slack_users_list):
    # print(slack_users_list)
    # model containing the users of slack
    for user in slack_users_list:
        slack_user = SlackUser.objects.get_or_create(uid=user['id'])
        # slack_user = SlackUser.objects.get(uid=user['id'])
        # print(slack_user)
        if 'real_name' in user and 'name' in user and 'email' in user['profile']:
            slack_user.name = user['real_name']
            slack_user.username = user['name']
            slack_user.email = user['profile']['email']
            slack_user.save()


def users_list():
    # returns the list of channels
    raw_data = raw_users_list()

    if not (len(raw_data['members']) == SlackUser.objects.count()):
        update_slack_members(raw_data['members'])

    if not raw_data['ok']:
        return None
    else:
        return raw_data['members']


def active_users():
    # returns the list of active users
    raw_users_data = users_list()
    active_users_list = []
    if raw_users_data is None:
        return None
    for user in raw_users_data:
        if 'presence' in user and user['presence'] == 'active':
            if 'name' in user and 'real_name' in user and 'email' in user['profile'] and 'id' in user:
                active_users_list.append({
                    'name': user['name'],
                    'real_name': user['real_name'],
                    'email': user['profile']['email'],
                    'id': user['id']
                })
    return active_users_list


def active_public_users():
    # returns the list of active users who are also members of public channel
    public_channel_users = public_channel_info()['members']
    active_users_list = active_users()
    if active_users_list is None or public_channel_users is None:
        return None
    active_public_users_list = []
    for user in active_users_list:
        if user['id'] in public_channel_users:
            active_public_users_list.append(user)
    return active_public_users_list


# {'members': ['U3SRS5L59'], 'name': 'public', 'num_members': 1, 'id': 'C8F1CQHT2'}
