'''VKYC project


1. Create a frontend where user will upload a short video and Photo ID
2. Write a function for uploading both files to S3 as soon as user clicks Upload/Submit
3. Write a function to read the video frame by frame and detect blinks and lip movement


links:
https://youtu.be/SIZNf_Ydplg?si=PbusvbWdRqjRzBSX
https://zoomout.medium.com/how-to-use-facial-landmarks-obtained-from-dlib-b82129e5b352
https://medium.com/@RiwajNeupane/facial-landmark-detection-a6b3e29eac5b
'''


import streamlit as st
import time 
import upload_to_s3 as upload
# title
st.title("Video KYC")

form = st.form("my_form")
img_upload = form.file_uploader("Upload Photo ID",type=['jpeg','png','jpg'],accept_multiple_files=False)
video_upload = form.file_uploader("Upload short video", type=['mp4','mkv'],accept_multiple_files=False)
submit = form.form_submit_button("Upload")

# validating a form 

if submit:
    if video_upload is None or img_upload is None:
         alert = st.warning("Please upload a file 💀💀")
         time.sleep(2)
         alert.empty()
    else:
        with st.spinner('Uploading......'):
            time.sleep(2)
        upload.upload_img_video_to_s3(img_upload,video_upload)
        upload.detect_blinks_in_video()
        
        st.snow()
