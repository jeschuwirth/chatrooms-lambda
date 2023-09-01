import os, boto3


def get_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    aws_table_name = os.environ[table_name]
    return dynamodb.Table(aws_table_name)
