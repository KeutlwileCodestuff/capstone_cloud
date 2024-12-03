import json
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb', 'eu-west-1')

# Table names
UNITS_TABLE = "StorageUnits"
BOOKINGS_TABLE = "StorageBookings"

def lambda_handler(event, context):
    # Parse the request body
    body = json.loads(event.get('body', '{}'))
    unit_id = body.get('unit_id')
    customer_id = body.get('customer_id')
    start_date = body.get('start_date')
    end_date = body.get('end_date')
    payment_method = body.get('payment_method')

    if not (unit_id and customer_id and start_date and end_date and payment_method):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required fields'})
        }

    try:
        # Validate dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if start >= end:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid date range'})
            }

        # Check unit availability
        units_table = dynamodb.Table(UNITS_TABLE)
        unit = units_table.get_item(Key={'id': unit_id}).get('Item')
        if not unit or unit['status'] != 'Available':
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unit not available'})
            }

        # Create a booking
        bookings_table = dynamodb.Table(BOOKINGS_TABLE)
        booking_id = str(uuid4())
        booking = {
            'id': booking_id,
            'unit_id': unit_id,
            'customer_id': customer_id,
            'start_date': start_date,
            'end_date': end_date,
            'payment_method': payment_method,
            'status': 'Confirmed'
        }
        bookings_table.put_item(Item=booking)

        # Update unit status
        units_table.update_item(
            Key={'id': unit_id},
            UpdateExpression="SET #status = :status",
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'Reserved'}
        )

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Storage unit booked successfully',
                'booking_id': booking_id,
                'unit_id': unit_id,
                'customer_id': customer_id,
                'start_date': start_date,
                'end_date': end_date
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }