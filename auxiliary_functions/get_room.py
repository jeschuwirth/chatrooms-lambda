from auxiliary_functions.get_table import get_table


def get_room(connection_id):
    connections_table = get_table("CONNECTIONS_TABLE")

    response = connections_table.get_item(
        Key = {
            'connection_id': connection_id
        },
        AttributesToGet = [
            'room_id',
        ]
    )
    if 'Item' in response:
        return response['Item']['room_id']
    return ''