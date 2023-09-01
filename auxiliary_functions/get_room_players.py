from auxiliary_functions.get_table import get_table


def get_room_players(room_id, only_active_players = True):
    players_table = get_table("PLAYERS_TABLE")

    return players_table.query(
        KeyConditions={
            'room_id': {
                'AttributeValueList': [room_id],
                'ComparisonOperator': 'EQ'
            }
        },
        QueryFilter={
            'connection_id': {
                'AttributeValueList': [None],
                'ComparisonOperator': 'NE'
            }
        } if only_active_players else {}
    )
