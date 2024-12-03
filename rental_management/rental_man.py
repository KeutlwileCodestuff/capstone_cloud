import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Rentals')

    payment_method = {
        'unit': event['unit'],
        'minNotice': event['minNotice'],
        'rentalDuration': event['rentalDuration'],
        'billingOption': event['billingOption']
    }

    table.put_item(Item=payment_method)
    return {
        'statusCode': 200,
        'body': 'Rental of unit cancelled successfully!'
    }

