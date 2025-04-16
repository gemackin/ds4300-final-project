import streamlit as st
import pandas as pd
import os
from analytics import *


# Directory to store uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def initialize_app():
    global UPLOADED_FILE, DESCRIPTION, SUBMIT_BUTTON
    st.title("Image Upload with Description and Color Analytics")
    # Form Section with Submit Button
    with st.form(key='image_upload_form'):
        UPLOADED_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        DESCRIPTION = st.text_input("Enter a description of the image")
        # Submit button
        SUBMIT_BUTTON = st.form_submit_button(label='Submit')
    

def populate_analytics():
    data = None # Not implemented yet
    # Analytics Section
    st.subheader("Analytics on Uploaded Images")

    # Display total uploads
    st.metric("Total Uploads", get_total_uploads(data))
    
    # Display most common colors
    st.subheader("Top Dominant Colors")
    try:
        common_colors = get_most_common_colors(data)
        st.write("Most common dominant colors:")
        for color, count in common_colors.items():
            st.text(f"{color}: {count}")
    except Exception as e:
        st.error(f"Could not load color analytics: {e}")
    
    # Display the RGB histograms for the uploaded images
    st.subheader("RGB Intensity Histograms")
    try:
        fig = plot_rgb_histograms(data)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Unable to display RGB histograms: {e}")


def read_input():
    # Waiting on the user click submit
    while not submit_button:
        pass
    metadata = {
        'filename': UPLOADED_FILE.name,
        'description': DESCRIPTION,
        'dominant_color': extract_dominant_color(UPLOADED_FILE.name)
    }
    return UPLOADED_FILE.read(), metadata
