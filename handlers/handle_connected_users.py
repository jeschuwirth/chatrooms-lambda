from botocore.exceptions import ClientError
import json

from auxiliary_functions.get_room import get_room
from auxiliary_functions.get_room_players import get_room_players
from auxiliary_functions.send_message import send_message

def handle_connected_users(event, connection_id, apig_management_client):
    status_code = 200
    room_id = get_room(connection_id)
    players = get_room_players(room_id, only_active_players = False)

    data = [{
        "username": p['user_name'],
        "is_active": p['connection_id'] != None
    } for p in players]

    message = json.dumps({
        "action": "connected_users",
        "body": data
    })

    for recipient in [p['connection_id'] for p in players]:
        if recipient != None:
            send_message(message, recipient, apig_management_client)

    return status_code

