import streamlit as st
import pandas as pd
import os
from analytics import (
    load_data, get_total_uploads,
    get_most_common_colors, extract_dominant_color,
    plot_rgb_histograms  
)

# Directory to store uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Image Upload with Description and Color Analytics")

# Form Section with Submit Button
with st.form(key='image_upload_form'):
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    description = st.text_input("Enter a description of the image")
   
    # Submit button
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if uploaded_file and description:
        image_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract dominant color
        dominant_color = extract_dominant_color(image_path)

        # Save metadata
        new_data = pd.DataFrame([{
            "filename": uploaded_file.name,
            "description": description,
            "dominant_color": dominant_color
        }])

        try:
            existing = pd.read_csv("uploaded_data.csv")
            all_data = pd.concat([existing, new_data], ignore_index=True)
        except FileNotFoundError:
            all_data = new_data

        all_data.to_csv("uploaded_data.csv", index=False)
        st.success(f"Upload saved! Dominant color: {dominant_color}")
    else:
        st.warning("Please upload an image and enter a description.")

# Analytics Section
st.subheader("Analytics on Uploaded Images")

data = load_data()

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
