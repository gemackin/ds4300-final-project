import streamlit as st
from .analytics import *


# Initial steps to setting up the web app UI
def initialize_app():
    populate_form() # There's nothing else here yet
    

# Adding the image upload form and analytics to UI
def populate_form(con=st):
    global UPLOADED_FILE, DESCRIPTION, SUBMIT_BUTTON
    con.title("Image Upload and Color Analytics")
    # Form Section with Submit Button
    with con.form(key='image_upload_form', clear_on_submit=True):
        UPLOADED_FILE = con.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        DESCRIPTION = con.text_input("Enter a description of the image")
        SUBMIT_BUTTON = con.form_submit_button(label='Submit')


# Updates the analytics section on the UI
def populate_analytics(con=st):
    filenames = get_filenames('preprocessed')
    # Display total uploads
    con.subheader("Analytics on Uploaded Images")
    con.metric("Total Uploads", get_total_uploads(filenames))
    # Display the RGB histograms for the uploaded images
    con.subheader("RGB Intensity Histograms")
    try:
        con.pyplot(plot_rgb_histograms(filenames))
    except Exception as e:
        con.error(f"Unable to display RGB histograms: {e}")


# Returns the state of the submit button
def get_submit_button():
    return SUBMIT_BUTTON


# Reads the inputted file and metadata from the UI
def read_input():
    metadata = {
        'filename': UPLOADED_FILE.name,
        'description': DESCRIPTION
    }
    return UPLOADED_FILE.getvalue(), metadata
