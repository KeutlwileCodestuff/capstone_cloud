import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PaymentMethods')

    payment_method = {
        'paymentMethodId': event['paymentMethodId'],
        'customerId': event['customerId'],
        'paymentType': event['paymentType'],
        'paymentDetails': event['paymentDetails']
    }

    table.put_item(Item=payment_method)
    return {
        'statusCode': 200,
        'body': 'Payment method added successfully!'
    }
