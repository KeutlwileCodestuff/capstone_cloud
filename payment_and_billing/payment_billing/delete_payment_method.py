import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    # Check if pathParameters is present and contains paymentMethodId
    if 'pathParameters' in event and 'paymentMethodId' in event['pathParameters']:
        payment_method_id = event['pathParameters']['paymentMethodId']
    else:
        logger.error("Missing path parameter: paymentMethodId")
        return {
            'statusCode': 400,
            'body': 'Missing path parameter: paymentMethodId'
        }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PaymentMethods')

    try:
        table.delete_item(Key={'paymentMethodId': payment_method_id})
        return {
            'statusCode': 200,
            'body': 'Payment method deleted successfully!'
        }
    except Exception as e:
        logger.error(f"Error deleting payment method: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Internal server error'
        }