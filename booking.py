import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, Blueprint
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import requests
import aws_controller
from PIL import Image
from cognito import send_email
import os
import botocore
import string
import random

APP_CLIENT_ID = "281hf825n7bh0t0s55giarg103"
dynamoRoute = Blueprint('dynamoRoute', __name__)

dynamodb = boto3.resource('dynamodb',  region_name='us-west-2')
dynamodb_client = boto3.client('dynamodb', region_name="us-west-2")

admin_Email = ''

@dynamoRoute.route('/create_booking', methods=['POST','GET'])
def create_booking():
    if request.method == 'POST':


        letters = string.ascii_lowercase
        booking_id=  ''.join(random.choice(letters) for i in range(10)) 
        client_name = request.form['cl_name']
        client_email = request.form['cl_email']
        admin_email = request.form['adm_email']
        time = request.form['time']
        date = request.form['date']
        meeting_name = request.form['meeting_name']

        r = requests.post('https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking',
            headers={"Authorization": session['idToken']},
            json= {"booking_id":booking_id, "client_name":client_name, "client_email":client_email, "time":time, "meeting_name":meeting_name, "date":date })



        return render_template("Adminhome.html")

    return render_template("booking.html")

@dynamoRoute.route('/get_booking', methods=['POST','GET'])
def get_bookings():


        r = requests.get('https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking',
            headers={"Authorization": session['idToken']})
        
        print(r.json())

        return render_template("getbookings.html")

@dynamoRoute.route('/delete_booking', methods=['POST','GET'])
def delete():
    table = dynamodb.Table('Bookings')

    # table = dynamodb.Table('practice_mapping')
    scan = table.query(
    KeyConditionExpression=Key('admin_email').eq('p@p.com')
    )
    with table.batch_writer() as batch:
        for item in scan['Items']:
            batch.delete_item(Key={'admin_email':item['admin_email'],'booking_id':item['booking_id']})
    # try:
    #     response = table.delete_item(
    #         Key={
    #             'admin_email': 'ali@ali.com',
    #         },
    #         ConditionExpression=" <= :val",
    #         ExpressionAttributeValues={
    #             'meeting_name': 's'
    #         }
    #     )
    
    # except ClientError as e:
    #     if e.response['Error']['Code'] == "ConditionalCheckFailedException":
    #         print(e.response['Error']['Message'])
    #     else:
    #         raise
    # else:
    #     return render_template("getbookings.html")

    # return response
    return render_template("getbookings.html")
