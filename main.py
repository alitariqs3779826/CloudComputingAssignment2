
import json
import boto3
from botocore.exceptions import ClientError

def profile(event, context):
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
    profile = {
        "name": "",
        "email": email,
        "contact": "",
        "password": ""
    }

    try:
        db = dynamodb_client.get_item(TableName ='Users', Key = {'email': {'S': email} })
        
        if "Item" in db and "name" in db.get("Item"):
            profile["name"] = db.get("Item").get("name").get("S", "")
        
        if "Item" in db and "contact" in db.get("Item"):
            profile["contact"] = db.get("Item").get("contact").get("S", "")
        
        if "Item" in db and "password" in db.get("Item"):
            profile["password"] = db.get("Item").get("password").get("S", "")
        

    except ClientError:
        return {
            "statusCode": 200,
            "body": json.dumps(profile)
        }


    return {
        "statusCode": 200,
        "body": json.dumps(profile)
    }
    
def update_profile(event, context):
    email = event.get("requestContext").get("authorizer").get("claims").get("email")
    dynamodb_client = boto3.client('dynamodb', region_name = "us-west-2")
    request_body = json.loads(event.get("body"))
    name = request_body.get("name","")

    contact = request_body.get("contact","")
    
    profile = {
        "name": "",
        "email": email,
        "contact": "",
        "password": ""
    }
    try:
        db = dynamodb_client.get_item(TableName ='Users', Key = {'email': {'S': email} })
        # profile["email"] = json.loads(event.get("body").get("email")) 
        # profile["name"] = json.loads(event.get("body").get("name")) 
        # profile["password"] = json.loads(event.get("body").get("password")) 
        # profile["contact"] = json.loads(event.get("body").get("contact")) 
        response = dynamodb_client.update_item(
            ExpressionAttributeNames={
                '#N': 'name',
                '#C': 'contact'
            },
            ExpressionAttributeValues={
                ':n': {
                    'S': name ,
                },
                ':c': {
                    'S': contact ,
                }  
            },
            Key={
                'email': {
                    'S': email,
                }
              
            },
            ReturnValues='ALL_NEW',
            TableName='Users',
            UpdateExpression='SET  #N = :n,#C = :c',
            )
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    except ClientError:
        response = dynamodb_client.put_item(TableName='Users',Item={ 'email': {'S': email},
                'name': {'S':name }, 'password': {'S':"Test"},'contact': {'S': contact } 
        },ReturnConsumedCapacity='TOTAL')
        
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
        

    return {
        "statusCode": 200,
        "body": json.dumps(profile.get("name"))
    }


    

