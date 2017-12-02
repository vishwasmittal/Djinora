from channels.handler import AsgiHandler
from channels import Channel, Group
from channels.sessions import channel_session


@channel_session
def ws_connect(message):
    pass


@channel_session
def ws_receive(message):
    pass


def ws_disconnect(message):
    pass