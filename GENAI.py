# streamlit_app.py

import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO
from PIL import Image
import os

# Configure your API key securely
api_key = os.getenv("GENAI_API_KEY")  # Use environment variable
if api_key is None:
    st.error("API key not found. Please set the GENAI_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)  
    model = genai.GenerativeModel("gemini-1.5-flash")

    st.title("Image to CSV Converter")

    # Upload an image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        # Generate CSV from image
        if st.button("Convert Image to CSV"):
            with st.spinner("Processing..."):
                try:
                    prompt = "Convert this image to CSV"
                    response = model.generate_content([prompt, img])
                    
                    if response and hasattr(response, 'text'):
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
                    else:
                        st.error("Error generating CSV. Please check the image and try again.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Uncomment to list available models
# st.subheader("Available Models")
# models = genai.list_models()
# for model in models:
#     st.write(f"**Model Name:** {model.name}")
#     st.write(f"**Description:** {model.description}")
#     st.write(f"**Supported Generation Methods:** {', '.join(model.supported_generation_methods)}")
