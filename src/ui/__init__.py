from .analytics import *
import streamlit as st


# Performs all operations associated with web app startup
def initialize_app():
    populate_app()


# Adds text and buttons to the web app
def populate_app():
    st.title('This is a title')
    st.write('## This is a subheader')


# Reads in uploaded files and metadata from web app
def read_input():
    uploaded_files = st.file_uploader(
        label='Choose a file',
        accept_multiple_files=True,
        type=['jpg', 'jpeg', 'png']
    )
    # TODO: Accept additional metadata beyond file name
    for file in uploaded_files:
        metadata = {'filename': file.name}
        yield file.read(), metadata