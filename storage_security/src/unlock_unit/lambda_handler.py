import json
import boto3

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='eu-west-1')
table = dynamodb.Table('StorageUnits')

def send_email(unit_id, user_email):
    ses.send_email(
        Source='lmaistry023@student.wethinkcode.co.za',
        Destination={'ToAddresses': [user_email]},
        Message={
            'Subject': {'Data': f"Unit {unit_id} Unlocked"},
            'Body': {'Text': {'Data': f"Unit {unit_id} has been unlocked."}}
        }
    )

def lambda_handler(event, context):
    unit_id = event['unit_id']
    user_email = event['user_email']

    table.update_item(
        Key={'unit_id': unit_id},
        UpdateExpression="SET #status = :available",
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':available': 'Available'}
    )

    send_email(unit_id, user_email)

    return {
        'statusCode': 200,
        'body': json.dumps('Unit unlocked and email notification sent')
    }
