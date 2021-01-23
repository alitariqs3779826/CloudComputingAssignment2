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
<<<<<<< Updated upstream
    response_booking = requests.get("https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking", 
    headers={"Authorization": session['idToken']})
    print(r.json()['Items'][0]['time'])

    return render_template("getbookings.html", client_name = r.json()['Items'][0]['client_name'], date = r.json()['Items'][0]['date']
    , time = r.json()['Items'][0]['time'], client_email = r.json()['Items'][0]['client_email'], meeting_name = r.json()['Items'][0]['meeting_name'] )

@dynamoRoute.route('/delete_booking', methods=['POST','GET'])
def delete():
    table = dynamodb.Table('Bookings')

    r = requests.delete('https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking',
            headers={"Authorization": session['idToken']})
=======
    number_of_elements = r.json()['Count']

    
    client_email = []
    client_name = []
    date = []
    time = []
    booking_id = []
    meeting_name = []

    for i in range(number_of_elements):
        client_email.append(r.json()['Items'][i]['client_email'])
        client_name.append(r.json()['Items'][i]['client_name'])
        date.append(r.json()['Items'][i]['date'])
        time.append(r.json()['Items'][i]['time'])
        booking_id.append(r.json()['Items'][i]['booking_id'])
        meeting_name.append(r.json()['Items'][i]['meeting_name'])

    print(request.form.get("booking_id"))
    
    if r:
        return render_template("getbookings.html", emails = client_email, names = client_name, dates = date, times = time
        , booking_ids = booking_id, meeting_names = meeting_name )
    
    return render_template("getbookings.html")

@dynamoRoute.route('/delete_booking', methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        print(client_name)
        table = dynamodb.Table('Bookings')
        r = requests.delete('https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking',
            headers={"Authorization": session['idToken']}, json= {"booking_id":booking_id})
>>>>>>> Stashed changes

    return render_template("getbookings.html")

@dynamoRoute.route('/edit_booking', methods=['POST','GET'])
def edit():
<<<<<<< Updated upstream
    # table = boto3.resource('dynamodb').Table('my_table')
    # print(session['idToken'])
    # response = table.get_item(Key={'admin_email': '7'})
    # item = response['Item']

    # item['meeting_name'] = 'PleaseJoinThis'

    # # put (idempotent)
    # table.put_item(Item=item)

    #
    r = requests.post('https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking',
            headers={"Authorization": session['idToken']},json= {"client_name":'name',"date":'contact',"time":'t',"client_email":'joe@joe.com',"meeting_name":'pLEASEJOINTHIS',"booking_id":'asad'})

    # table = boto3.resource('dynamodb').Table('Bookings')

    # table.update_item(
    #     Key={'admin_email': 'kuch@bhi.com'},
    #     AttributeUpdates={
    #         'meeting_name': 'hujabhai'
    #     },
    # )
    return render_template("getbookings.html")
=======
    r = requests.post('https://1r77dpeab4.execute-api.us-west-2.amazonaws.com/dev/booking',
            headers={"Authorization": session['idToken']},json= {"client_name":'name',"date":'contact',"time":'t',"client_email":'joe@joe.com',"meeting_name":'pLEASEJOINTHIS',"booking_id":'asad'})

    return render_template("getbookings.html")
>>>>>>> Stashed changes
