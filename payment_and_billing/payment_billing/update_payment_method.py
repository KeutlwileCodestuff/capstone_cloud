import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    # Parse the JSON body
    try:
        body = json.loads(event['body'])
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Invalid JSON or missing body: {str(e)}")
        return {
            'statusCode': 400,
            'body': 'Invalid JSON or missing body'
        }
    
    payment_method_id = event['pathParameters']['paymentMethodId']
    required_keys = ['customerId', 'paymentType', 'paymentDetails']
    
    for key in required_keys:
        if key not in body:
            logger.error(f"Missing key: {key}")
            return {
                'statusCode': 400,
                'body': f"Missing key: {key}"
            }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PaymentMethods')

    update_expression = "SET customerId = :customerId, paymentType = :paymentType, paymentDetails = :paymentDetails"
    expression_attribute_values = {
        ':customerId': body['customerId'],
        ':paymentType': body['paymentType'],
        ':paymentDetails': body['paymentDetails']
    }

    try:
        table.update_item(
            Key={'paymentMethodId': payment_method_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {
            'statusCode': 200,
            'body': 'Payment method updated successfully!'
        }
    except Exception as e:
        logger.error(f"Error updating payment method: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Internal server error'
        }