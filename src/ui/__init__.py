import streamlit as st
from .analytics import *


# Initial steps to setting up the web app UI
def initialize_app():
    global UPLOADED_FILE, DESCRIPTION, SUBMIT_BUTTON, EXIT_BUTTON
    EXIT_BUTTON = st.button(label='Shut down application') # Doesn't work? Beats me why
    st.title("Image Upload with Description and Color Analytics")
    # Form Section with Submit Button
    with st.form(key='image_upload_form'):
        UPLOADED_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        DESCRIPTION = st.text_input("Enter a description of the image")
        SUBMIT_BUTTON = st.form_submit_button(label='Submit')
    populate_analytics(empty=False)


# Updates the analytics section on the UI
def populate_analytics(empty=False):
    filenames = [] if empty else get_filenames('preprocessed')
    # Display total uploads
    st.subheader("Analytics on Uploaded Images")
    st.metric("Total Uploads", get_total_uploads(filenames))
    # Display the RGB histograms for the uploaded images
    st.subheader("RGB Intensity Histograms")
    try:
        st.pyplot(plot_rgb_histograms(filenames))
    except Exception as e:
        st.error(f"Unable to display RGB histograms: {e}")


# Reads the inputted file and metadata from the UI
def read_input():
    metadata = {
        'filename': UPLOADED_FILE.name,
        'description': DESCRIPTION
    }
    return UPLOADED_FILE.read(), metadata
