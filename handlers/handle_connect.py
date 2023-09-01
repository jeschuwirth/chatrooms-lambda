from botocore.exceptions import ClientError

from auxiliary_functions.get_table import get_table

def handle_connect(event, connection_id, apig_management_client):
    status_code = 200
    user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')
    room_id = event.get('queryStringParameters', {'room': "aaaa"}).get("room")

    try:
        create_or_activate_player(connection_id, room_id, user_name)
        create_connection(connection_id, room_id, user_name)

    except ClientError:
        status_code = 505

    return status_code


def create_connection(connection_id, room_id, user_name):
    connections_table = get_table('CONNECTIONS_TABLE')
    return connections_table.put_item(Item={
        'connection_id': connection_id,
        'room_id': room_id,
        'user_name': user_name,
    })


def create_or_activate_player(connection_id, room_id, user_name):
    players_table = get_table('PLAYERS_TABLE')
    response = players_table.get_item(Key = {"room_id": room_id, "user_name": user_name})

    # If the player exists
    if 'Item' in response:
        if (response['Item']['connection_id']):
            raise ClientError
        return players_table.update_item(
            Key = {"room_id": room_id, "user_name": user_name},
            AttributeUpdates = {
                'connection_id': {
                'Action': 'PUT',
                'Value': connection_id
            }}
        )

    # Otherwise create the player
    return players_table.put_item(Item={
        'room_id': room_id, 
        'user_name': user_name,
        'connection_id': connection_id,
        'is_host': False
    })