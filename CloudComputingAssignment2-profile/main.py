
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import boto3
from botocore.exceptions import ClientError
import requests
import aws_controller
from PIL import Image
import os
import botocore
from cognito import cognitoRoute
from s3 import s3Route


app = Flask(__name__)
APP_CLIENT_ID = "281hf825n7bh0t0s55giarg103"
app.config["IMAGE_UPLOADS"] = "static/img"
app.secret_key = '281hf825n7bh0t0s55giarg103'

app.register_blueprint(s3Route)
app.register_blueprint(cognitoRoute)
# app.register_blueprint(passwordRoute)

# dbName = ''
# dbContact = ''

# logged_username = ''
# logged_password = ''

# @app.route('/')
# def lobby():
#     return render_template('index.html')


# @app.route('/auth/signup/', methods=['POST'])
# def signup():
#     user_email = request.form['Email']
#     user_password = request.form['Password']
#     user_name = request.form['Username']

#     idp_client = boto3.client('cognito-idp')
#     try:
#         idp_client.sign_up(ClientId=APP_CLIENT_ID,
#                            Username=user_email,
#                            Password=user_password,
#                            UserAttributes=[{'Name': 'name', 'Value': user_name}])
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UsernameExistsException':
           
#             print("User already exists")
#         if e.response['Error']['Code'] == 'ParamValidationError':
          
#             print("Param Validate Error")
#         print(e)
#     return redirect(url_for('lobby'))


# @app.route('/auth/resend/confirm/', methods=['POST'])
# def resend_confirm():
#     user_email = request.form['Email']

#     idp_client = boto3.client('cognito-idp')
#     try:
#         idp_client.resend_confirmation_code(ClientId=APP_CLIENT_ID,
#                                             Username=user_email)
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UserNotFoundException':
         
#             print("Can't Find user by Email")
#         if e.response['Error']['Code'] == 'ParamValidationError':
         
#             print("Param Validate Error")
#         print(e)
#     return redirect(url_for('lobby'))


# @app.route('/auth/confirm/signup/', methods=['POST'])
# def confirm_sign_up():
#     user_email = request.form['Email']
#     confirm_code = request.form['ConfirmCode']

#     idp_client = boto3.client('cognito-idp')
#     try:
#         idp_client.confirm_sign_up(ClientId=APP_CLIENT_ID,
#                                    Username=user_email,
#                                    ConfirmationCode=confirm_code)
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UserNotFoundException':
#             # Todo Handle Not Found User
#             print("Can't Find user by Email")
#         if e.response['Error']['Code'] == 'CodeMismatchException':
#             # Todo Handle Code Mismatch
#             print("User Code Mismatch")
#         if e.response['Error']['Code'] == 'ParamValidationError':
#             # Todo Handle Param Validate
#             print("Param Validate Error")
#         if e.response['Error']['Code'] == 'ExpiredCodeException':
#             # Todo Handle Expired Code
#             print("Expired Code")
#         print(e)
#     return redirect(url_for('lobby'))


# @app.route('/auth/forgot/password/', methods=['POST'])
# def forgot_password():
#     user_email = request.form['Email']

#     idp_client = boto3.client('cognito-idp')
#     try:
#         idp_client.forgot_password(ClientId=APP_CLIENT_ID,
#                                    Username=user_email)
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UserNotFoundException':
         
#             print("Can't Find user by Email")
#         if e.response['Error']['Code'] == 'ParamValidationError':
            
#             print("Param Validate Error")
#         print(e)
#     return redirect(url_for('lobby'))

# @app.route('/auth/login', methods=['GET','POST'])
# def login():
#     user_email = request.form['Email']
#     password = request.form['Password']

#     idp_client = boto3.client('cognito-idp')
#     response = None
#     try:
#         response =  idp_client.initiate_auth(ClientId=APP_CLIENT_ID,
#                                     AuthFlow='USER_PASSWORD_AUTH',
#                                     AuthParameters={
#                                     'USERNAME': user_email,
#                                     'PASSWORD': password
#                                     }
#         )
#         session['idToken'] = response['AuthenticationResult']['IdToken']

#         # global logged_username
#         # logged_username  = user_email
#         session['username'] = user_email
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UserNotFoundException':
          
#             print("Can't Find user by Email")
#             return redirect(url_for('lobby'))
#         if e.response['Error']['Code'] == 'ParamValidationError':
            
#             print("Param Validate Error")
#             return redirect(url_for('lobby'))
#         print(e)
    
      
  

#     r = requests.get("https://8c7ymla190.execute-api.us-west-2.amazonaws.com/dev/test_auth", 
#     headers={"Authorization": response['AuthenticationResult']['IdToken']})
#     print(response['AuthenticationResult']['IdToken'])
   
#     return redirect(url_for('home'))

# @app.route('/dashboard')
# def home():
#     return render_template('home.html')

# @app.route('/profile')
# def profile():
#     # os.remove(os.path.join(app.config["IMAGE_UPLOADS"], str(session['username'])+".png"))
#     r = requests.get("https://xomyksdc28.execute-api.us-west-2.amazonaws.com/dev/profile", 
#     headers={"Authorization": session['idToken']})

#     global dbName 
#     global dbContact 

#     dbName = r.json()['name']
#     dbContact = r.json()['contact']
#     download_image(r.json()['email'])
#     # image_object = s3 lookup based on file-name
#     # get url of image
#     # if image not uploaded - get default image path (can be local)
#     # path = app.config["IMAGE_UPLOADS"]+"/"+r.json()['email']+".png"
#     s3_client = boto3.client('s3', region_name='us-west-2')
#     url = s3_client.generate_presigned_url('get_object',
#                                 Params={
#                                     'Bucket': 'profilebucket',
#                                     'Key': r.json()['email']+".png",
#                                 },                                  
#                                 ExpiresIn=3600)
#     print(url)
    
#     return render_template('profile.html',name = r.json()['name'],contact = r.json()['contact'],email = r.json()['email'], password = r.json()['password'],user_image = url)

# @app.route('/get-items')
# def get_items():
#     return jsonify(aws_controller.get_items())

# @app.route('/auth/confirm/forgot/password/', methods=['POST'])
# def confirm_forgot_password():
#     user_email = request.form['Email']
#     confirm_code = request.form['ConfirmCode']
#     random_password = '!1a+random'

#     idp_client = boto3.client('cognito-idp')
#     try:
#         idp_client.confirm_forgot_password(ClientId=APP_CLIENT_ID,
#                                            Username=user_email,
#                                            ConfirmationCode=confirm_code,
#                                            Password=random_password)

#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UserNotFoundException':
          
#             print("Can't Find user by Email")
#         if e.response['Error']['Code'] == 'CodeMismatchException':
#             print("User Code Mismatch")
#         if e.response['Error']['Code'] == 'ParamValidationError':
           
#             print("Param Validate Error")
#         if e.response['Error']['Code'] == 'ExpiredCodeException':
#             print("Expired Code")

#     return redirect(url_for('lobby'))

# @app.route('/edit_profile',methods=['GET','POST'])
# def editProfile():
#     if request.method  == 'POST':
#         print("h")
#         name = request.form['name']
#         email = request.form['email']
#         contact = request.form['contact']
#         password = request.form['password']
#         if request.files:
        
#             s3_client = boto3.client('s3', region_name='us-west-2')
#             image = request.files["image"]
#             print(session['username'])
#             image.save(os.path.join(app.config["IMAGE_UPLOADS"], str(session['username'])+".png"))
   
            
#             try:

                
#                 path = app.config["IMAGE_UPLOADS"]+"/"+str(session['username'])+".png"
#                 print(image)
#                 if image.filename != '':
#                     image_exists(str(session['username']))
#                     s3_client.upload_file(str(path), 'profilebucket', str(session['username'])+".png")
#                 # else:
#                 #     response = s3_client.upload_file(str(path), 'profilebucket', str(session['username'])+".png")
#             except ClientError as e:
#                 print(e)
#                 print("no")
#                 return None
#         os.remove(os.path.join(app.config["IMAGE_UPLOADS"], str(session['username'])+".png"))
#         r = requests.post('https://xomyksdc28.execute-api.us-west-2.amazonaws.com/dev/profile',
#         headers={"Authorization": session['idToken']},json= {"name":name,"contact":contact})

#         # return redirect(url_for(profile))


#     return render_template('edit_profile.html', name = dbName, password = "password", email = "email", contact = dbContact)

# def createBucket():
   
#     client = boto3.client('s3')
#     try:

#         response = client.create_bucket(
#         Bucket='profilebucket',
#         CreateBucketConfiguration={
#             'LocationConstraint': 'us-west-2',
#         },)
        
#         print(response)

#     except ClientError as e:
#         print(e)
#         print("no")
        
#     return None

# def download_image(name):
#     s3 = boto3.resource('s3')
#     path = app.config["IMAGE_UPLOADS"]+"/"+str(name)+".png"
#     s3.meta.client.download_file('profilebucket', name+".png", path)

# def image_exists(name):
   
#     s3 = boto3.resource('s3')
#     s3_client = boto3.client('s3', region_name='us-west-2')
#     path = app.config["IMAGE_UPLOADS"]+"/"+str(session['username'])+".png"
#     try:
#         s3.Object('profilebucket', str(name)+".png").load()
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == "404":
     
            
#             s3_client.upload_file(str(path), 'profilebucket', str(session['username'])+".png")
#             print("not")
#             return 
#         else:
       
#             print("g")

#     print("exsists")
 
    

if __name__ == '__main__':
   
    app.run(debug=True)