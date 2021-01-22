
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def booking(event, context):
    
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    booking = {
        "admin_email":email,
        "booking_id":"",
        "meeting_name":"",
        "client_name":"",
        "client_email":"",
        "date":"",
        "time":""
    }

    dynamodb = boto3.resource('dynamodb',  region_name='us-west-2')

    try: 
        table = dynamodb.Table('Bookings')
        response = table.query(
            KeyConditionExpression=Key('admin_email').eq(email)
        )


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
        "body": json.dumps('profile')
    }
    
def create_booking(event, context):
    
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
    request_body = json.loads(event.get("body"))
    booking_id = request_body.get("booking_id","")
    meeting_name = request_body.get("meeting_name","")
    client_name = request_body.get("client_name","")
    client_email = request_body.get("client_email","")
    date = request_body.get("date","")
    time = request_body.get("time","")


    booking = {
        "admin_email":email,
        "booking_id":"",
        "meeting_name":"",
        "client_name":"",
        "client_email":"",
        "date":"",
        "time":""
    }


    try: 
        response = dynamodb_client.put_item(
            TableName='Bookings',
            Item={ 
                'admin_email': {
                    'S': email
                    },
                'booking_id': {
                    'S': booking_id 
                    }, 
                'meeting_name': {
                    'S': meeting_name
                },
                 'client_name': {
                    'S': client_name
                },
                'client_email': {
                    'S': client_email
                },
                'date': {
                    'S': date
                },
                'time': {
                    'S': time
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
