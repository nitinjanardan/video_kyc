#Libraries

import streamlit as st
from dotenv import load_dotenv
import os
import boto3
import time,datetime
from datetime import datetime
import time
import cv2
import dlib
from scipy.spatial import distance
#---------------------------------------------------------------------
#AWS Cred
#  Aws cred
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("region")
bucket_name  = os.getenv("bucket_name")
local_path = os.getenv("local_path")
#----------------------------------------------------------------------

# initializing boto client globally for all function
s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name = region)

# ------------------------------------------------
# defining global variable for storing image and video vlaues
video_file_name_loc = None
image_file_name_loc = None


# function for reading file and uploading to S3 bucket
def upload_img_video_to_s3(img_upload,video_upload):
    global video_file_name_loc,image_file_name_loc
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
        filename_loc = f'{folder}/{file}'
    alert= st.success(f'file uploaded succesfully')
    time.sleep(2)
    alert.empty()
    video_file_name_loc = os.path.join(os.getcwd(),video)
    image_file_name_loc = os.path.join(os.getcwd(),img)
    # st.write(os.path.join(os.getcwd(),video))

def eye_aspect_ratio(eye):
    """Calculate Eye Aspect Ratio (EAR) for blink detection."""
    A = distance.euclidean(eye[1], eye[5])  # Vertical distance
    B = distance.euclidean(eye[2], eye[4])  # Vertical distance
    C = distance.euclidean(eye[0], eye[3])  # Horizontal distance
    EAR = (A + B) / (2.0 * C)
    return EAR

def detect_blinks_in_video():
    """Calculate the number of blinks in a video."""
    # Load the face detector and landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # fetching image and video values
    video_path = video_file_name_loc
    image_path = image_file_name_loc
    file_name = [image_path,video_path]

    # Define EAR threshold and consecutive frame limit
    EAR_THRESHOLD = 0.25
    CONSEC_FRAMES = 2

    # Blink counters
    blink_counter = 0
    total_blinks = 0

    # Read video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            shape = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

            left_eye = shape[36:42]
            right_eye = shape[42:48]

            # Compute EAR for both eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0

            if ear < EAR_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= CONSEC_FRAMES:
                    total_blinks += 1
                blink_counter = 0

    cap.release()
    st.write("Total Number of blink: ",total_blinks)
    # Removing file from local system
    for del_file in file_name:
        local_path_dir = os.path.join(os.getcwd(),del_file)

        os.remove(local_path_dir)

    