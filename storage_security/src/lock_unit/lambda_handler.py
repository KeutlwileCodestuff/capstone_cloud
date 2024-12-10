import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StorageUnits')

def lambda_handler(event, context):
    unit_id = event['unit_id']

    table.update_item(
        Key={'unit_id': unit_id},
        UpdateExpression="SET #status = :locked",
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':locked': 'Locked'}
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Unit {unit_id} locked successfully')
    }
