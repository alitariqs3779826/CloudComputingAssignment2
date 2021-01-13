import boto3
import json

with open('happy.jpg', 'rb') as image_data:
    response_content = image_data.read()

def detect_faces(photo):

    client=boto3.client('rekognition',aws_access_key_id='ASIAXCDX35MMYLRMLFJC',
             aws_secret_access_key='wZg/J0K1J3zDfVYaNfF7g989xKqBBT313SpBasua',
             aws_session_token='FwoGZXIvYXdzEB4aDG09R52nL11YckLRkSLMAX8mJPY4gyZNkZpFcRpm/XSWZgfpfyeLUVKJLQxf2AE3APIAEhzjdFa8bLiIMSkBWKAj6kFcXAQ6mOJQovD/CIsG6BXYEDr0e4XJvhWlRxsDKb928VF5gpCXly5BT6JxaVveKC377jCnZTYUA+TYJ2BVO+niUDi3aVFLpWBEhYUulFmWdiNviA6Rr4A/0zRQdW1JYlKlNTBSE6mmMgvxtKB4qdVs1r+4l573vrXF8t871XB4I02yhvUrxAkorjhX+zaB8nf1PLluYKA9VCjjxfv/BTIttsxPs8837c8EuEuJBQK89AJSqlzKGK34KVurU2rEHRrVQ3f3AZYO+YnZ/GDJ',
             region_name='us-east-1')

    response = client.detect_faces(Image={'Bytes':response_content}, Attributes=['ALL'])

    print('Detected faces for ' + photo)    
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))

    return len(response['FaceDetails'])

def main():
    photo='happy.jpg'
    face_count=detect_faces(photo)
    print("Faces detected: " + str(face_count))


if __name__ == "__main__":
    main()