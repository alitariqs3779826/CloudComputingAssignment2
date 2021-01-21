
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
config = "static/img"
# app.secret_key = '281hf825n7bh0t0s55giarg103'

s3Route = Blueprint('s3Route', __name__)

dbName = ''
dbContact = ''

logged_username = ''
logged_password = ''



@s3Route.route('/profile')
def profile():
    print(session['idToken'])
    # os.remove(os.path.join(app.config["IMAGE_UPLOADS"], str(session['username'])+".png"))
    r = requests.get("https://xomyksdc28.execute-api.us-west-2.amazonaws.com/dev/profile", 
    headers={"Authorization": session['idToken']})
    
    global dbName 
    global dbContact 

    session['name'] = r.json()['name']
    session['contact'] = r.json()['contact']
    # download_image(r.json()['email'])
    # image_object = s3 lookup based on file-name
    # get url of image
    # if image not uploaded - get default image path (can be local)
    # path = app.config["IMAGE_UPLOADS"]+"/"+r.json()['email']+".png"
    # s3 = boto3.resource('s3')
    # s3.Object('profilebucket', str(name)+".png").load()
    s3_client = boto3.client('s3', region_name='us-west-2')
    url = s3_client.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'profilebucket',
                                    'Key': r.json()['email']+".png",
                                },                                  
                                ExpiresIn=3600)
    print(url)
    
    return render_template('profile.html',name = r.json()['name'],contact = r.json()['contact'],email = r.json()['email'], password = r.json()['password'],user_image = url)

@s3Route.route('/get-items')
def get_items():
    return jsonify(aws_controller.get_items())



@s3Route.route('/edit_profile',methods=['GET','POST'])
def editProfile():
    if request.method  == 'POST':
        print("h")
        name = request.form['name']
        # email = request.form['email']
        contact = request.form['contact']
        # password = request.form['password']
        if request.files:
        
            s3_client = boto3.client('s3', region_name='us-west-2')
            image = request.files["image"]
            print(session['username'])
            image.save(os.path.join(config, str(session['username'])+".png"))
   
            
            try:

                
                path = config+"/"+str(session['username'])+".png"
                print(image)
                print(str(session['username']))
                if image.filename != '':
                    # image_exists(str(session['username']))
                    s3_client.upload_file(str(path), 'profilebucket', str(session['username'])+".png")
                # else:
                #     response = s3_client.upload_file(str(path), 'profilebucket', str(session['username'])+".png")
            except ClientError as e:
                print(e)
                print("no")
                return None
        os.remove(os.path.join(config, str(session['username'])+".png"))
        r = requests.post('https://xomyksdc28.execute-api.us-west-2.amazonaws.com/dev/profile',
        headers={"Authorization": session['idToken']},json= {"name":name,"contact":contact})

        return redirect(url_for('s3Route.profile'))

     


    return render_template('edit_profile.html', name = session['name'], password = "password", email = "email", contact =  session['contact'])

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

def download_image(name):
    s3 = boto3.resource('s3')
    path = config+"/"+str(name)+".png"
    s3.meta.client.download_file('profilebucket', name+".png", path)

def image_exists(name):
   
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3', region_name='us-west-2')
    path = config+"/"+str(session['username'])+".png"
    try:
        s3.Object('profilebucket', str(name)+".png").load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
     
            
            s3_client.upload_file(str(path), 'profilebucket', str(session['username'])+".png")
            print("not")
            return 
        else:
       
            print("g")

    print("exsists")
 
    