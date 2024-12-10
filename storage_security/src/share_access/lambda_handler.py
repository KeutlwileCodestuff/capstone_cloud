import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SharedAccess')

def lambda_handler(event, context):
    unit_id = event['unit_id']
    shared_user_id = event['shared_user_id']
    access_period = event['access_period']

    table.put_item(
        Item={
            'unit_id': unit_id,
            'shared_user_id': shared_user_id,
            'access_period': access_period
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Access granted for user {shared_user_id} to unit {unit_id}')
    }
