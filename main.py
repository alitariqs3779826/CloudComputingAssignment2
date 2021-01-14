# from pycognito import Cognito

# u = Cognito('us-west-2_PsC9h5W0N', '281hf825n7bh0t0s55giarg103')

# u.set_base_attributes(email='you@you.com', password='random value')

# u.register('username', 'password')
import os
from flask import Flask, render_template, redirect, url_for, request
import boto3
from botocore.exceptions import ClientError
import requests

app = Flask(__name__)
APP_CLIENT_ID = "281hf825n7bh0t0s55giarg103"


@app.route('/')
def lobby():
    return render_template('index.html')


@app.route('/auth/signup/', methods=['POST'])
def signup():
    user_email = request.form['Email']
    user_password = request.form['Password']
    user_name = request.form['Username']

    idp_client = boto3.client('cognito-idp')
    try:
        idp_client.sign_up(ClientId=APP_CLIENT_ID,
                           Username=user_email,
                           Password=user_password,
                           UserAttributes=[{'Name': 'name', 'Value': user_name}])
    except ClientError as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            # Todo Handle Already Exists Email
            print("User already exists")
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            print("Param Validate Error")
        print(e)
    return redirect(url_for('lobby'))


@app.route('/auth/resend/confirm/', methods=['POST'])
def resend_confirm():
    user_email = request.form['Email']

    idp_client = boto3.client('cognito-idp')
    try:
        idp_client.resend_confirmation_code(ClientId=APP_CLIENT_ID,
                                            Username=user_email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # Todo Handle Not Found User
            print("Can't Find user by Email")
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            print("Param Validate Error")
        print(e)
    return redirect(url_for('lobby'))


@app.route('/auth/confirm/signup/', methods=['POST'])
def confirm_sign_up():
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
    return redirect(url_for('lobby'))


@app.route('/auth/forgot/password/', methods=['POST'])
def forgot_password():
    user_email = request.form['Email']

    idp_client = boto3.client('cognito-idp')
    try:
        idp_client.forgot_password(ClientId=APP_CLIENT_ID,
                                   Username=user_email)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # Todo Handle Not Found User
            print("Can't Find user by Email")
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            print("Param Validate Error")
        print(e)
    return redirect(url_for('lobby'))

@app.route('/auth/login', methods=['GET','POST'])
def login():
    user_email = request.form['Email']
    password = request.form['Password']

    idp_client = boto3.client('cognito-idp')
    response = None
    try:
        response =  idp_client.initiate_auth(ClientId=APP_CLIENT_ID,
                                    AuthFlow='USER_PASSWORD_AUTH',
                                    AuthParameters={
                                    'USERNAME': user_email,
                                    'PASSWORD': password
                                    }
        )
        # idp_client.login(ClientId=APP_CLIENT_ID,
        #                            Username=user_email,
        #                            password =password)
        
                
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # Todo Handle Not Found User
            print("Can't Find user by Email")
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            print("Param Validate Error")
        print(e)
    
    r = requests.get("https://8c7ymla190.execute-api.us-west-2.amazonaws.com/dev/test_auth", 
    headers={"Authorization": response['AuthenticationResult']['IdToken']})

    print(r)

    return render_template('home.html')

@app.route('/auth/confirm/forgot/password/', methods=['POST'])
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

    return redirect(url_for('lobby'))


if __name__ == '__main__':
    app.run()