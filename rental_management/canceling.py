import json
import boto3
from datetime import datetime

def overSixMonths(start_date , end_date):
      
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    difference_in_months = (end.year - start.year) * 12 + (end.month - start.month)
    if difference_in_months < 6:
        return False
    else:
        return True
def lambda_handler(event):

    dynamodb = boto3.client("dynamodb" , region_name = "eu-west-1")

    response = dynamodb.scan(TableName = "BookedUnits")
    tableContent = response["Items"]
    try:
        for i in tableContent:
            if i.get("ID") == event:
                allowed = overSixMonths(i["startDate"]["S"] , i["endDate"]["S"])
                if allowed:
                    tableContent.remove(i)
                    return{
                        "status":200 , 
                        "body":"Rental unit cancelled successfully!"
                    }
                    
                else:
                    return{
                        "status":400,
                        "body":"You are not allowed to cancel rental unit"
                    }
                   
    except Exception as e:
        return{
            "status":500,
            "body":"'error':e"
        }

# lambda_handler({'S': '02'})
