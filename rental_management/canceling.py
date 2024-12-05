import json
import boto3

from datetime import datetime


def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))

    unit_id = body.get('unit_id')
    customer_id = body.get('customer_id')
    start_date = body.get('start_date')
    end_date = body.get('end_date')
    payment_method = body.get('payment_method')

    if not (unit_id or start_date or end_date or payment_method):
        return{
            'statusCode':400,
            'body':json.dumps({'error':'Missing required fields'})
        }

    try:
        allowed = overSixMonths(start_date , end_date)
        if allowed:
            return{
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Storage unit cancelled successfully',
                        'unit_id': unit_id,
                        'customer_id': customer_id,
                        'start_date': start_date,
                        'end_date': end_date
            })
        }

        else:
            return{
                'statusCode':403,
                'body':json.dumps({'error':'Not allowed to cancel.'})
            }

    except Exception as e:
        return {
        'statusCode': 500,
        'body': json.dumps({'error': str(e)})
        }

def overSixMonths(start_date , end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    difference_in_months = (end.year - start.year) * 12 + (end.month - start.month)
    if difference_in_months < 6:
        return False
    else:
        return True