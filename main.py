
import json
import boto3
from botocore.exceptions import ClientError

def booking(event, context):
    

    return {
        "statusCode": 200,
        "body": json.dumps('profile')
    }
    
def create_booking(event, context):
    
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
    request_body = json.loads(event.get("body"))
    booking_id = request_body.get("booking_id","")
    meeting_name = request_body.get("meeting_name","")

    dynamodb = boto3.resource('dynamodb',  region_name='us-west-2')

    table = dynamodb.Table("Bookings")

    booking = {
        "admin_email":email,
        "booking_id":"",
        "meeting_name":""
    }


    try: 
        response = dynamodb_client.put_item(
            TableName='Bookings',
            Item={ 
                'admin_email': {
                    'S': email
                    },
                'booking_id': {
                    'S':booking_id 
                    }, 
                'meeting_name': {
                    'S':meeting_name
                } 
            },ReturnConsumedCapacity='TOTAL')


        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }

    except ClientError:
        return {
            "statusCode": 200,
            "body": json.dumps(booking)
        }

    return {
        "statusCode": 200,
        "body": json.dumps('profile.get("name")')
    }
