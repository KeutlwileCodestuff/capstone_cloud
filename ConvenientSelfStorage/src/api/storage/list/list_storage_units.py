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
    },
    {
        "id": "unit125",
        "facility": "Uptown Storage",
        "town": "Johannesburg",
        "size": "locker",
        "status": "Available",
        "price": 250
    },
    {
        "id": "unit126",
        "facility": "Midtown Storage",
        "town": "Pretoria",
        "size": "double garage",
        "status": "Available",
        "price": 1500
    },
    {
        "id": "unit127",
        "facility": "Rosebank Storage",
        "town": "Rosebank",
        "size": "small storage unit",
        "status": "Unavailable",
        "price": 800
    },
    {
        "id": "unit128",
        "facility": "Durban Self-Storage",
        "town": "Durban",
        "size": "single garage",
        "status": "Available",
        "price": 1100
    },
    {
        "id": "unit129",
        "facility": "Northside Storage",
        "town": "Pietersburg",
        "size": "medium storage unit",
        "status": "Available",
        "price": 900
    },
    {
        "id": "unit130",
        "facility": "Phalaborwa Secure Storage",
        "town": "Phalaborwa",
        "size": "locker",
        "status": "Unavailable",
        "price": 300
    },
    {
        "id": "unit131",
        "facility": "Coastal Storage",
        "town": "Durban",
        "size": "double garage",
        "status": "Available",
        "price": 1600
    },
    {
        "id": "unit132",
        "facility": "Downtown Depot",
        "town": "Rosebank",
        "size": "single garage",
        "status": "Unavailable",
        "price": 1300
    },
    {
        "id": "unit133",
        "facility": "Central Storage",
        "town": "Johannesburg",
        "size": "locker",
        "status": "Available",
        "price": 250
    },
    {
        "id": "unit134",
        "facility": "Pretoria Storage Hub",
        "town": "Pretoria",
        "size": "small storage unit",
        "status": "Available",
        "price": 750
    },
    {
        "id": "unit135",
        "facility": "Phalaborwa Vaults",
        "town": "Phalaborwa",
        "size": "double garage",
        "status": "Available",
        "price": 1400
    }
]

    
    # Populate table with temporary data
    for item in temp_data:
        try:
            table.put_item(Item=item)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f"Failed to add item {item['id']}: {str(e)}"})
            }
    
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
