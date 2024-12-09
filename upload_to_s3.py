#Libraries

import streamlit as st
from dotenv import load_dotenv
import os
import boto3
import time,datetime
from datetime import datetime
import time
#---------------------------------------------------------------------
#AWS Cred
#  Aws cred
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
#AWS_DEFAULT_REGION = "ap-south-1"
region = os.getenv("region")
bucket_name  = os.getenv("bucket_name")
local_path = os.getenv("local_path")
#----------------------------------------------------------------------

# initializing boto client globally for all function
s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name = region)

# function for reading file and uploading to S3 bucket
def upload_img_video_to_s3(img_upload,video_upload):
    img = img_upload.name
    # splitting the image name 

    img_name = img.split(".")
    video = video_upload.name

    # reading the image and video 
    
    with open(img,"wb") as f:
        f.write(img_upload.getvalue())
    with open(video,"wb") as f:
        f.write(video_upload.getvalue())

    # storing the variable in list
    file_name = [img,video]
    
    # fetching current date time-------------------------
    date_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    # creating folder ---------------------------
    folder =f'{img_name[0]}-{date_time}'
    s3.put_object(Bucket=bucket_name, Key=(folder+'/'))

    # uploading file into s3 bucket
    for file in file_name:
        upload = s3.upload_file(file,bucket_name,f'{folder}/{file}')
    alert= st.success(f'file uploaded succesfully')
    time.sleep(2)
    alert.empty()
    
    # Removing file from local system
    for del_file in file_name:
        local_path_dir = os.path.join(os.getcwd(),del_file)
        os.remove(local_path_dir)
    

    