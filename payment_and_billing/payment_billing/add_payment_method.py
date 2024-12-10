import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    # Parse the JSON body
    try:
        body = json.loads(event['body'])  # Parse the stringified JSON inside 'body'
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Invalid JSON or missing body: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins
                'Access-Control-Allow-Methods': 'POST, OPTIONS',  # Allow specific methods
                'Access-Control-Allow-Headers': 'Content-Type'  # Allow specific headers
            },
            'body': json.dumps({'message': 'Invalid JSON or missing body'})
        }
    
    required_keys = ['paymentMethodId', 'customerId', 'paymentType', 'paymentDetails']
    
    # Check if all required keys are present in the body
    for key in required_keys:
        if key not in body:
            logger.error(f"Missing key: {key}")
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'message': f"Missing key: {key}"})
            }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PaymentMethods')

    payment_method = {
        'paymentMethodId': body['paymentMethodId'],
        'customerId': body['customerId'],
        'paymentType': body['paymentType'],
        'paymentDetails': body['paymentDetails']
    }

    try:
        table.put_item(Item=payment_method)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Payment method added successfully!'})
        }
    except Exception as e:
        logger.error(f"Error adding payment method: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Internal server error'})
        }
