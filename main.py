
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def booking(event, context):
    
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    # dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
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
    #     db = dynamodb_client.get_item(TableName ='Bookings', Key = {'admin_email': {'S': email} })

    #     if "Item" in db and "client_name" in db.get("Item"):
    #         booking["client_name"] = db.get("Item").get("client_name").get("S", "")
        
    #     if "Item" in db and "client_email" in db.get("Item"):
    #         booking["client_email"] = db.get("Item").get("client_email").get("S", "")
        
    #     if "Item" in db and "time" in db.get("Item"):
    #         booking["time"] = db.get("Item").get("time").get("S", "")

    #     if "Item" in db and "date" in db.get("Item"):
    #         booking["date"] = db.get("Item").get("date").get("S", "")

    #     if "Item" in db and "meeting_name" in db.get("Item"):
    #         booking["meeting_name"] = db.get("Item").get("meeting_name").get("S", "")

    #     if "Item" in db and "booking_id" in db.get("Item"):
    #         booking["booking_id"] = db.get("Item").get("booking_id").get("S", "")


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

    # def update_booking():
    #     email = event.get("requestContext").get("authorizer").get("claims").get("email")
        
    #     dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
        
    #     request_body = json.loads(event.get("body"))
        
    #     booking_id = request_body.get("booking_id","")
    #     meeting_name = request_body.get("meeting_name","")
    #     date = request_body.get("date","")
    #     time = request_body.get("time","")
    #     client_name = request_body.get("client_name","")
    #     client_email = request_body.get("client_email","")

    #     return {
    #             "statusCode": 200,
    #             "body": json.dumps(client_email)
    #         }

    #     booking = {
    #         "admin_email":email,
    #         "booking_id":"",
    #         "meeting_name":"",
    #         "client_name":"",
    #         "client_email":"",
    #         "date":"",
    #         "time":""
    #     }

    #     try:
    #         db = dynamodb_client.get_item(TableName ='Bookings', Key = {'admin_email': {'S': email} })
    #         # profile["email"] = json.loads(event.get("body").get("email")) 
    #         # profile["name"] = json.loads(event.get("body").get("name")) 
    #         # profile["password"] = json.loads(event.get("body").get("password")) 
    #         # profile["contact"] = json.loads(event.get("body").get("contact")) 
    #         response = dynamodb_client.update_item(
    #             ExpressionAttributeNames={
    #                 '#B': 'booking_id',
    #                 '#M': 'meeting_name',
    #                 '#C': 'client_name',
    #                 '#E': 'client_email',
    #                 '#D': 'date',
    #                 '#T': 'time'
    #             },
    #             ExpressionAttributeValues={
    #                 ':b': {
    #                     'S': booking_id ,
    #                 },
    #                 ':m': {
    #                     'S': meeting_name ,
    #                 },
    #                 ':c': {
    #                     'S': client_name ,
    #                 },
    #                 ':e': {
    #                     'S': client_email ,
    #                 },
    #                 ':d': {
    #                     'S': date ,
    #                 },
    #                 ':t': {
    #                     'S': time ,
    #                 }       
    #             },
    #             Key={
    #                 'admin_email': {
    #                     'S': email,
    #                 }
    #             },
    #             ReturnValues='ALL_NEW',
    #             TableName='Bookings',
    #             UpdateExpression='SET  #B = :b,#M = :m,#C = :c,#E = :e,#D = :d,#T = :t',
    #             )
    #         return {
    #             "statusCode": 200,
    #             "body": json.dumps(response)
    #         }
    #     except ClientError:
    #         response = dynamodb_client.put_item(TableName='Bookings',Item={ 'admin_email': {'S': email},
    #                 'client_name': {'S': client_name }, 'client_email': {'S': client_email},'date': {'S': date }, 'time': {'S': time }, 'booking_id': {'S': booking_id }
    #                 , 'meeting_name': {'S': meeting_name }    
    #         },ReturnConsumedCapacity='TOTAL')
            
    #         return {
    #             "statusCode": 200,
    #             "body": json.dumps(response)
    #         }
            

    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps(booking.get("client_name"))
    #     }
