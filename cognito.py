
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, Blueprint
import boto3
from botocore.exceptions import ClientError
import requests
import aws_controller
from PIL import Image
import os
import botocore


APP_CLIENT_ID = "281hf825n7bh0t0s55giarg103"


dynamodb = boto3.resource('dynamodb',  region_name='us-west-2')
dynamodb_client = boto3.client('dynamodb', region_name="us-west-2")

cognitoRoute = Blueprint('cognitoRoute', __name__)

send_email =''


@cognitoRoute.route('/contact', methods=['GET'])
def contact_page():
    return render_template('contact.html')

@cognitoRoute.route('/Adminhome')
def admin_home():
    return render_template('Adminhome.html')

@cognitoRoute.route('/Userhome')
def user_home():
    return render_template('home.html')

@cognitoRoute.route('/auth/signup')
def create_account():
    return signup()

@cognitoRoute.route('/about')
def about_page():
    return render_template("about.html")

@cognitoRoute.route('/')
def login_page():
    return redirect(url_for('cognitoRoute.login'))

@cognitoRoute.route('/auth/forgot/password/')
def forget_password_page():
    return render_template('forgot_password.html')



@cognitoRoute.route('/auth/signup/', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_email = request.form['Email']
        user_password = request.form['Password']
        user_name = request.form['Username']
        idp_client = boto3.client('cognito-idp')
        usertype = request.form['usertype']

        try:
            idp_client.sign_up(ClientId=APP_CLIENT_ID,
                            Username=user_email,
                            Password=user_password,
                            UserAttributes=[{'Name': 'name', 'Value': user_name}])
        except ClientError as e:
            if e.response['Error']['Code'] == 'UsernameExistsException':
                
                print("User already exists")
                return redirect(url_for('cognitoRoute.create_account'))
            if e.response['Error']['Code'] == 'ParamValidationError':
                
                print("Param Validate Error")
                return redirect(url_for('cognitoRoute.create_account'))
            print(e)


        r = requests.post('https://xomyksdc28.execute-api.us-west-2.amazonaws.com/dev/add_usertype_profile',
        json= {"name":user_name,"email":user_email,"usertype":usertype})

        return redirect(url_for('cognitoRoute.login'))


    return render_template('create_account.html')


@cognitoRoute.route('/auth/resend/confirm/', methods=['POST'])
def resend_confirm():
    user_email = request.form['Email']

    idp_client = boto3.client('cognito-idp')
    try:
        idp_client.resend_confirmation_code(ClientId=APP_CLIENT_ID,
                                            Username=user_email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
         
            print("Can't Find user by Email")
        if e.response['Error']['Code'] == 'ParamValidationError':
         
            print("Param Validate Error")
        print(e)
    return redirect(url_for('cognitoRoute.lobby'))


@cognitoRoute.route('/auth/confirm/signup/', methods=['POST'])
def confirm_sign_up():
    if request.method == 'POST':
        user_email = request.form['Email']
        confirm_code = request.form['ConfirmCode']

        idp_client = boto3.client('cognito-idp')
        try:
            idp_client.confirm_sign_up(ClientId=APP_CLIENT_ID,
                                        Username=user_email,
                                        ConfirmationCode=confirm_code)
        except ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                # Todo Handle Not Found User
                print("Can't Find user by Email")
            if e.response['Error']['Code'] == 'CodeMismatchException':
                # Todo Handle Code Mismatch
                print("User Code Mismatch")
            if e.response['Error']['Code'] == 'ParamValidationError':
                # Todo Handle Param Validate
                print("Param Validate Error")
            if e.response['Error']['Code'] == 'ExpiredCodeException':
                # Todo Handle Expired Code
                print("Expired Code")
            print(e)
    return redirect(url_for('signup_confirmation_page'))


@cognitoRoute.route('/auth/forgot/password/', methods=['POST'])
def forgot_password():
    user_email = request.form['Email']

    idp_client = boto3.client('cognito-idp')
   
    try:
        idp_client.forgot_password(ClientId=APP_CLIENT_ID,
                                   Username=user_email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            
            print("Can't Find user by Email")
            return redirect(url_for('cognitoRoute.forget_password_page'))
        if e.response['Error']['Code'] == 'ParamValidationError':
            
            print("Param Validate Error")
            return redirect(url_for('cognitoRoute.forget_password_page'))
    
    return redirect(url_for('cognitoRoute.login'))

    print(e)

    return redirect(url_for('cognitoRoute.forget_password_page'))

@cognitoRoute.route('/auth/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['Email']
        password = request.form['Password']

        idp_client = boto3.client('cognito-idp')
        response = None
        
        global send_email
        


        try:
            response =  idp_client.initiate_auth(ClientId=APP_CLIENT_ID,
                                        AuthFlow='USER_PASSWORD_AUTH',
                                        AuthParameters={
                                        'USERNAME': user_email,
                                        'PASSWORD': password
                                        }
            )
            session['idToken'] = response['AuthenticationResult']['IdToken']


            
            session['username'] = user_email


        except ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                
                print("Can't Find user by Email")
                return redirect(url_for('cognitoRoute.login_page'))
            if e.response['Error']['Code'] == 'ParamValidationError':
                
                print("Param Validate Error")
                return redirect(url_for('cognitoRoute.login_page'))
            print(e)

        r = requests.get("https://8c7ymla190.execute-api.us-west-2.amazonaws.com/dev/test_auth", 
        headers={"Authorization": response['AuthenticationResult']['IdToken']})
        response_usertype = requests.get("https://xomyksdc28.execute-api.us-west-2.amazonaws.com/dev/profile", 
        headers={"Authorization": session['idToken']})
        print(response_usertype.json()['usertype'])
        session['token'] = response['AuthenticationResult']['AccessToken']
        print(session['token'])

        dynamo_userType = response_usertype.json()['usertype']

        if dynamo_userType == 'Normal':
            return redirect(url_for('cognitoRoute.user_home'))
        elif dynamo_userType == 'Admin':
            print("I went here")
            return redirect(url_for('cognitoRoute.admin_home'))
        

        


        return render_template("home.html")
   
    return render_template('login.html')

@cognitoRoute.route('/dashboard')
def home():
    return render_template('home.html')


@cognitoRoute.route('/auth/confirm/forgot/password/', methods=['POST'])
def confirm_forgot_password():
    user_email = request.form['Email']
    confirm_code = request.form['ConfirmCode']
    random_password = '!1a+random'

    idp_client = boto3.client('cognito-idp')
    try:
        idp_client.confirm_forgot_password(ClientId=APP_CLIENT_ID,
                                           Username=user_email,
                                           ConfirmationCode=confirm_code,
                                           Password=random_password)

    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
          
            print("Can't Find user by Email")
        if e.response['Error']['Code'] == 'CodeMismatchException':
            print("User Code Mismatch")
        if e.response['Error']['Code'] == 'ParamValidationError':
           
            print("Param Validate Error")
        if e.response['Error']['Code'] == 'ExpiredCodeException':
            print("Expired Code")

    return redirect(url_for('cognitoRoute.lobby'))


def return_email():
    return send_email