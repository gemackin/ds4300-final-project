import streamlit as st
import pandas as pd
import os
from analytics import *


def initialize_app():
    global UPLOADED_FILE, DESCRIPTION, SUBMIT_BUTTON
    st.title("Image Upload with Description and Color Analytics")
    # Form Section with Submit Button
    with st.form(key='image_upload_form'):
        UPLOADED_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        DESCRIPTION = st.text_input("Enter a description of the image")
        SUBMIT_BUTTON = st.form_submit_button(label='Submit')
    

def populate_analytics():
    filenames = get_filenames('preprocessed')
    # Display total uploads
    st.subheader("Analytics on Uploaded Images")
    st.metric("Total Uploads", get_total_uploads(filenames))
    # Display the RGB histograms for the uploaded images
    st.subheader("RGB Intensity Histograms")
    try:
        st.pyplot(plot_rgb_histograms(filenames))
    except Exception as e:
        st.error(f"Unable to display RGB histograms: {e}")


def read_input():
    # Waiting on the user click submit
    while not SUBMIT_BUTTON:
        pass
    metadata = {
        'filename': UPLOADED_FILE.name,
        'description': DESCRIPTION
    }
    return UPLOADED_FILE.read(), metadata
