
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


    except ClientError:
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }


    return {
        "statusCode": 200,
        "body": json.dumps(response)
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

def delete_booking(event, context):
    
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    request_body = json.loads(event.get("body"))
    booking_id = request_body.get("booking_id","")
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
        
        
        table = dynamodb.Table('Bookings')
        table.delete_item(
            Key={
                'admin_email': email,
                'booking_id': booking_id
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps('hello')
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

def update_booking(event, context):

    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    
    dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
    
    request_body = json.loads(event.get("body"))
    booking_id = request_body.get("booking_id","")

    meeting_name = request_body.get("meeting_name","")
    date = request_body.get("date","")
    time = request_body.get("time","")
    client_name = request_body.get("client_name","")
    client_email = request_body.get("client_email","")

    booking = {
        "admin_email":email,
        "booking_id":booking_id,
        "meeting_name":"",
        "client_name":"",
        "client_email":"",
        "date":"",
        "time":""
    }

    try:
        response = dynamodb_client.update_item(
        ExpressionAttributeNames={
            '#M': 'meeting_name',
            '#C': 'client_name',
            '#E': 'client_email',
            '#D': 'date',
            '#T': 'time'
        },
        ExpressionAttributeValues={
            ':m': {
                'S': meeting_name ,
            },
            ':c': {
                'S': client_name ,
            },
            ':e': {
                'S': client_email ,
            },
            ':d': {
                'S': date,
            },
            ':t': {
                'S': time ,
            }       
        },
        Key={
            'admin_email': {
                'S': email,
            },
            'booking_id': {
                'S': booking_id,
            }
        },
        ReturnValues='ALL_NEW',
        TableName='Bookings',
        UpdateExpression='SET  #M = :m,#C = :c,#E = :e,#D = :d,#T = :t',
        )
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    except ClientError:
        response = dynamodb_client.put_item(TableName='Bookings',Item={ 'admin_email': {'S': email},
                'client_name': {'S': client_name }, 'client_email': {'S': client_email},'date': {'S': date }, 'time': {'S': time }, 'booking_id': {'S': booking_id }
                , 'meeting_name': {'S': meeting_name }    
        },ReturnConsumedCapacity='TOTAL')
        
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
        

    return {
        "statusCode": 200,
        "body": json.dumps(booking.get("client_name"))
    }

    
def get_client_bookings(event, context):
    dynamodb_client = boto3.client('dynamodb', region_name="us-west-2")
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

    try:
        response = dynamodb_client.scan(
        ExpressionAttributeNames={
            '#AT': 'client_name',
            '#ST': 'booking_id',
            '#TT': 'time',
            '#DT': 'date',
            '#MN': 'meeting_name'
        },
        ExpressionAttributeValues={
            ':a': {
                'S': email,
            },
        },
        FilterExpression='client_email = :a',
        ProjectionExpression='#ST, #AT, #TT, #DT, #MN',
        TableName='Bookings',
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
        "body": json.dumps("client_name")
    }
