from botocore.exceptions import ClientError

def send_message(message, recipient, apig_management_client):
    status_code = 200
    apig_management_client.post_to_connection(Data=message, ConnectionId=recipient)

    return status_code