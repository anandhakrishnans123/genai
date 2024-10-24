# streamlit_app.py

import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO
from PIL import Image

# Make sure to replace this with your actual API key
genai.configure(api_key="AIzaSyBA3sUF2AFbcYwrsuY7zVu38dB-pOA-v9c")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Image to CSV Converter")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Generate text from image

        # Generate CSV from image
    if st.button("Convert Image to CSV"):
        prompt = "image to csv"
        response = model.generate_content([prompt, img])
        csv_result = response.text
            
            # Use StringIO to simulate a file-like object for pandas
        data_io = StringIO(csv_result)
        
        # Read the data into a DataFrame
        df = pd.read_csv(data_io)
            
            # Save the DataFrame to a CSV file
        csv_file_path = 'csv_output.csv'
        df.to_csv(csv_file_path, index=False)
            
        st.success(f"CSV file saved as {csv_file_path}")
        st.write(df)  # Display the DataFrame
            
            # Provide a download link
        with open(csv_file_path, "rb") as f:
                st.download_button("Download CSV", f, file_name=csv_file_path)

# List available models
# st.subheader("Available Models")
# models = genai.list_models()
# for model in models:
#     st.write(f"**Model Name:** {model.name}")
#     st.write(f"**Description:** {model.description}")
#     st.write(f"**Supported Generation Methods:** {', '.join(model.supported_generation_methods)}")
