
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
import boto3
from botocore.exceptions import ClientError
import requests
import aws_controller
from PIL import Image
import os

app = Flask(__name__)
APP_CLIENT_ID = "281hf825n7bh0t0s55giarg103"
app.config["IMAGE_UPLOADS"] = "/Users/apple/Desktop/CloudComputingAssignment2/static/img"


logged_username = ''
logged_password = ''
dbName = ' '
dbPassword = ' '
dbMail = ' '
dbContact = ' '
userExists = True
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
      
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # Todo Handle Not Found User
            print("Can't Find user by Email")
            return redirect(url_for('lobby'))
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            print("Param Validate Error")
            return redirect(url_for('lobby'))
        print(e)
    
      
    global logged_username
    global logged_password
    logged_username = user_email
    logged_password = password

    r = requests.get("https://8c7ymla190.execute-api.us-west-2.amazonaws.com/dev/test_auth", 
    headers={"Authorization": response['AuthenticationResult']['IdToken']})

   
    return redirect(url_for('home'))

@app.route('/dashboard')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
   
    
  
    client = boto3.client('dynamodb',region_name="us-west-2")
    global dbName
    global dbMail
    global dbContact
    global dbPassword
    global userExists

    try:
        response = client.get_item(TableName='Users',Key={'email': {'S': "mail2@mail2.com"}})
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
        
            print("here")
    if response['ResponseMetadata']['HTTPHeaders']['content-length'] == str(2):
        dbName = ' '
        dbPassword = ' '
        dbMail = ' '
        dbContact = ' '
        userExists = False
    else:
        dbName = response['Item']['name']['S']
        dbPassword = response['Item']['password']['S']
        dbMail = response['Item']['email']['S']
        dbContact = response['Item']['contact']['S']
 
    return render_template('profile.html', name = dbName, password = dbPassword, email = dbMail, contact = dbContact)

@app.route('/get-items')
def get_items():
    return jsonify(aws_controller.get_items())

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

@app.route('/edit_profile',methods=['GET','POST'])
def editProfile():
    client = boto3.client('dynamodb',region_name="us-west-2")
    if request.method  == 'POST':
        print("h")
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        if userExists == False:
            try:
                response = client.put_item(TableName='Users',Item={ 'email': {'S': str(email)},
                'name': {'S':str(name)}, 'password': {'S':str(password)},'contact': {'S':str(contact)} 
                },ReturnConsumedCapacity='TOTAL')
                print(response)
            
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    print("Error")
        elif userExists == True:
            print("h")
            response = client.update_item(
            ExpressionAttributeNames={
                
                '#N': 'name',
                '#C': 'contact',
                '#P': 'password'
            },
            ExpressionAttributeValues={
                
                ':n': {
                    'S': str(name),
                },
                ':c': {
                    'S': str(contact),
                },
                ':p': {
                    'S': str(password),
                }
            },
            Key={
                'email': {
                    'S': 'mail2@mail2.com',
                }
              
            },
            ReturnValues='ALL_NEW',
            TableName='Users',
            UpdateExpression='SET  #N = :n,#C = :c, #P = :p',
            )
            print(response)
        



    return render_template('edit_profile.html', name = dbName, password = dbPassword, email = dbMail, contact = dbContact)

def createBucket():
   
    client = boto3.client('s3')
    try:

        response = client.create_bucket(
        Bucket='profilebucket',
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2',
        },)
        
        print(response)

    except ClientError as e:
        print(e)
        print("no")
        
    return None

def uploadImage():
    client = boto3.client('s3', region_name='us-west-2')
    try:
        response = client.upload_file('/Users/apple/Desktop/CloudComputingAssignment2/eso1907a.jpg', 'profilebucket', 'image_0.jpg')
        print(response)
    except ClientError as e:
        print(e)
        print("no")

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
           
            client = boto3.client('s3', region_name='us-west-2')
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            saved = True
            print(image)
            
            try:
                path = app.config["IMAGE_UPLOADS"]+"/"+str(image.filename)
                response = client.upload_file(str(path), 'profilebucket', image.filename)
                print(response)
            except ClientError as e:
                print(e)
                print("no")
            if saved == True:
                os.remove(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
        # if request.files:

        #     image = request.files["image"]
        #     image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
        #     os.remove(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
           

            return redirect(request.url)
    return render_template("upload_image.html")

if __name__ == '__main__':
   
    app.run(debug=True)