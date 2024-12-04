import boto3
import json
from decimal import Decimal

def lambda_handler(event, context):
    # Parse the JSON body
    try:
        body = json.loads(event['body'])
    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'body': 'Invalid JSON or missing body'
        }
    
    required_keys = ['billingId', 'facilityType', 'discountType']
    
    for key in required_keys:
        if key not in body:
            return {
                'statusCode': 400,
                'body': f"Missing key: {key}"
            }
    
    billing_id = body['billingId']
    facility_type = body['facilityType']
    discount_type = body['discountType']
    
    dynamodb = boto3.resource('dynamodb')
    discounts_table = dynamodb.Table('Discounts')
    billing_table = dynamodb.Table('Billing')
    
    # Retrieve the discount
    try:
        response = discounts_table.get_item(
            Key={
                'discountId': f"{facility_type}_{discount_type}"
            }
        )
        discount = response.get('Item')
        if not discount:
            return {
                'statusCode': 404,
                'body': 'Discount not found'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error retrieving discount: {str(e)}"
        }
    
    discount_value = Decimal(str(discount['discountValue']))
    
    # Retrieve the billing record
    try:
        response = billing_table.get_item(
            Key={
                'billingId': billing_id
            }
        )
        billing_record = response.get('Item')
        if not billing_record:
            return {
                'statusCode': 404,
                'body': 'Billing record not found'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error retrieving billing record: {str(e)}"
        }
    
    # Apply the discount
    original_amount = billing_record['amount']
    discounted_amount = original_amount - (original_amount * discount_value / 100)
    
    # Update the billing record with the discounted amount
    try:
        billing_table.update_item(
            Key={
                'billingId': billing_id
            },
            UpdateExpression="SET amount = :amount, discountApplied = :discountApplied",
            ExpressionAttributeValues={
                ':amount': discounted_amount,
                ':discountApplied': f"{discount_type} ({discount_value}%)"
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'originalAmount': str(original_amount),
                'discountedAmount': str(discounted_amount),
                'discountApplied': f"{discount_type} ({discount_value}%)"
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error updating billing record: {str(e)}"
        }