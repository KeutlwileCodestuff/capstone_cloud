import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # DynamoDB table
    table_name = "StorageUnits"
    dynamodb = boto3.resource('dynamodb', 'eu-west-1')
    table = dynamodb.Table(table_name)
    
    # Extract query parameters
    params = event.get('queryStringParameters', {})
    town = params.get('town')
    size = params.get('size')
    availability = params.get('availability')
    
    # Build filter expression
    filter_expression = []
    if town:
        filter_expression.append(Attr('town').eq(town))
    if size:
        filter_expression.append(Attr('size').eq(size))
    if availability:
        filter_expression.append(Attr('status').eq(availability))
    
    # Combine filters
    final_filter = None
    if filter_expression:
        final_filter = filter_expression[0]
        for f in filter_expression[1:]:
            final_filter = final_filter & f
    
    # Query DynamoDB
    try:
        if final_filter:
            response = table.scan(FilterExpression=final_filter)
        else:
            response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
