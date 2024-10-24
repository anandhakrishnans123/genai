import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO
from PIL import Image
import os
import tempfile

# Load API key from an environment variable
api_key = os.getenv("GENAI_API_KEY")  # Set your environment variable
genai.configure(api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Image to Text and CSV Converter")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Generate text from image
    if st.button("Convert Image to Text"):
        prompt = "image to text"
        response = model.generate_content([prompt, img])
        
        if response:
            text_result = response.text
            st.subheader("Extracted Text:")
            st.write(text_result)
        else:
            st.error("Failed to extract text from the image.")

        # Generate CSV from image
        if st.button("Convert Image to CSV"):
            prompt = "image to csv"
            response = model.generate_content([prompt, img])
            
            if response:
                csv_result = response.text
                # Use StringIO to simulate a file-like object for pandas
                data_io = StringIO(csv_result)
                
                try:
                    # Read the data into a DataFrame
                    df = pd.read_csv(data_io)
                    # Create a temporary file to save the DataFrame
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                        csv_file_path = tmp_file.name
                        df.to_csv(csv_file_path, index=False)
                    
                    st.success(f"CSV file saved as {csv_file_path}")
                    st.write(df)  # Display the DataFrame
                    
                    # Provide a download link
                    with open(csv_file_path, "rb") as f:
                        st.download_button("Download CSV", f, file_name=os.path.basename(csv_file_path))
                except Exception as e:
                    st.error(f"Error reading the CSV data: {e}")
            else:
                st.error("Failed to generate CSV from the image.")

# List available models
st.subheader("Available Models")
models = genai.list_models()
for model in models:
    st.write(f"**Model Name:** {model.name}")
    st.write(f"**Description:** {model.description}")
    st.write(f"**Supported Generation Methods:** {', '.join(model.supported_generation_methods)}")
