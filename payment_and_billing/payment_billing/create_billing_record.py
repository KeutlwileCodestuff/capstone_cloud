import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Billing')

    billing_record = {
        'billingId': event['billingId'],
        'customerId': event['customerId'],
        'amount': event['amount'],
        'billingType': event['billingType'],  # Pre-pay or Recurring
        'discountApplied': event.get('discountApplied', 'None')
    }

    table.put_item(Item=billing_record)
    return {
        'statusCode': 200,
        'body': 'Billing record created successfully!'
    }
