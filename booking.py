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
        table = dynamodb.Table('Bookings')
        global admin_Email
        letters = string.ascii_lowercase
        booking_ID=  ''.join(random.choice(letters) for i in range(10)) 
        client_Name = request.form['cl_name']
        client_Email = request.form['cl_email']
        admin_Email = request.form['adm_email']
        time = request.form['time']
        date = request.form['date']
        meeting_Name = request.form['meeting_name']

        insert_data = {}
        # print(str(send_email))

        insert_data['admin_email'] = str(admin_Email)
        insert_data['client_name'] = str(client_Name)
        insert_data['client_email'] = str(client_Email)
        insert_data['booking_id'] = str(booking_ID)
        insert_data['date'] = str(date)
        insert_data['time'] = str(time)
        insert_data['meeting_name'] = str(meeting_Name)

        print(insert_data)
        table.put_item(Item=insert_data)

        return render_template("Adminhome.html")

    return render_template("booking.html")

@dynamoRoute.route('/get_booking', methods=['POST','GET'])
def get_bookings():
        # print(admin_Email)

        
        # dyresponse = table.query(
        # KeyConditionExpression=Key('admin_email').eq('ali@k.com'))

        # print(dyresponse['Items'])

        # dynamo_response = dynamodb_client.get_item(
        #         TableName='Bookings',
        #         Key={'booking_id': {'S' : '12'}})

        # dynamo_userType = dynamo_response['Item']['admin_email']['S']
        # print(dynamo_userType)
        # response = dynamodb_client.batch_get_item(RequestItems={
        #     'Bookings': {
        #         'Keys': [{
        #             'admin_email':{
        #                 'S': 'ali@ali.com'
        #             }
        #         }
        #         ], 
        #         'AttributesToGet':['meeting_name'],
        #     },  
        # })
        # print(response)

        table = dynamodb.Table('Bookings')
        response = table.query(
        KeyConditionExpression=Key('admin_email').eq('ali@ali.com')
        )
        # return response['Items']
        print(response)

        return render_template("getbookings.html")
