from auxiliary_functions.get_table import get_table 
from auxiliary_functions.get_room_players import get_room_players


def delete_room_if_empty(room_id):
    room_players = get_room_players(room_id, only_active_players = False)
    any_active = any(p['connection_id'] for p in room_players['Items'])
    if any_active:
        return
    
    players_table = get_table("PLAYERS_TABLE")

    with players_table.batch_writer() as batch:
        for player in room_players['Items']:
            batch.delete_item(
                Key={'room_id': room_id, 'user_name': player['user_name']}
            )