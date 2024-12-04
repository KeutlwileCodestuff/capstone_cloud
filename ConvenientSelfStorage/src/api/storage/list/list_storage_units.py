import boto3
import json
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

def decimal_to_native(obj):
    """
    Convert DynamoDB Decimal types to native Python types for JSON serialization.
    """
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        # Convert Decimal to int if it's a whole number, else to float
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def lambda_handler(event, context):
    # DynamoDB table
    table_name = "StorageUnits"
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(table_name)
    
    # Temporary data to populate the table
    temp_data = [
        {
            "id": "unit123",
            "facility": "Downtown Storage",
            "town": "Cape Town",
            "size": "locker",
            "status": "Available",
            "price": 200
        },
        {
            "id": "unit124",
            "facility": "City Center Storage",
            "town": "Cape Town",
            "size": "single garage",
            "status": "Unavailable",
            "price": 1200
        }
    ]
    
    # Populate table with temporary data
    # for item in temp_data:
    #     try:
    #         table.put_item(Item=item)
    #     except Exception as e:
    #         return {
    #             'statusCode': 500,
    #             'body': json.dumps({'error': f"Failed to add item {item['id']}: {str(e)}"})
    #         }
    
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
        
        # Convert Decimal to native types for JSON serialization
        items = decimal_to_native(response['Items'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
