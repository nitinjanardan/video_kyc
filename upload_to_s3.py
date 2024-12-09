#Libraries

import streamlit as st
from dotenv import load_dotenv
import os
import boto3
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
    video = video_upload.name
    # reading the image and video 
    with open(img,"wb") as f:
        f.write(img_upload.getvalue())
    with open(video,"wb") as f:
        f.write(video_upload.getvalue())
    # storing the variable in list
    file_name = [img,video]
    # uploading file into s3 bucket
    for file in file_name:
        upload = s3.upload_file(file,bucket_name,file)
    alert= st.success(f'file uploaded succesfully to {bucket_name}')
    time.sleep(2)
    alert.empty()
    # Removing file from local system
    for del_file in file_name:
        local_path_dir = os.path.join(os.getcwd(),del_file)
        os.remove(local_path_dir)
    alert= st.success(f'file remove from locale')
    time.sleep(2)
    alert.empty()
    

    