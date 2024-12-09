'''VKYC project


1. Create a frontend where user will upload a short video and Photo ID
'''


import streamlit as st
import time 
import upload_to_s3 as up
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
        st.spinner("uploading........")
        up.upload_img_video_to_s3(img_upload,video_upload)