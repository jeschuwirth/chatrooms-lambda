from botocore.exceptions import ClientError

from auxiliary_functions.get_table import get_table
from auxiliary_functions.delete_room_if_empty import delete_room_if_empty

def handle_disconnect(event, connection_id, apig_management_client):
    status_code = 200

    try:
        user_name, room_id = delete_connection(connection_id)
        deactivate_player(room_id, user_name)
        delete_room_if_empty(room_id)

    except ClientError:
        status_code = 503

    return status_code


def delete_connection(connection_id):
    connections_table = get_table('CONNECTIONS_TABLE')
    response = connections_table.get_item(Key = {"connection_id": connection_id})
    if not ("Item" in response):
        raise ClientError
    user = response['Item']

    connections_table.delete_item(Key = {
        "connection_id": connection_id
    })
    return user['user_name'], user['room_id']


def deactivate_player(room_id, user_name):
    players_table = get_table('PLAYERS_TABLE')

    return players_table.update_item(
        Key = {"room_id": room_id, "user_name": user_name},
        AttributeUpdates = {
            'connection_id': {
            'Action': 'PUT',
            'Value': None
        }}
    )