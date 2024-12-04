import boto3
from decimal import Decimal
import json

def lambda_handler(event, context):
    # Log the event to see what is being passed to the Lambda function
    print(f"Received event: {json.dumps(event)}")
    
    # Parse the body if it's passed as a string
    if 'body' in event:
        event = json.loads(event['body'])

    # Check if the required fields exist in the event
    if 'billingId' not in event or 'customerId' not in event or 'amount' not in event or 'billingType' not in event:
        return {
            'statusCode': 400,
            'body': 'Missing required fields: billingId, customerId, amount, billingType'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Billing')

    billing_record = {
        'billingId': event['billingId'],
        'customerId': event['customerId'],
        'amount': Decimal(str(event['amount'])),  # Convert float to Decimal
        'billingType': event['billingType'],  # Pre-pay or Recurring
        'discountApplied': event.get('discountApplied', 'None')
    }

    table.put_item(Item=billing_record)
    return {
        'statusCode': 200,
        'body': 'Billing record created successfully!'
    }
