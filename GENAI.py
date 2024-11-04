import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO
from PIL import Image

st.title("Image to CSV Converter")

# Input for API key
api_key = st.text_input("Enter your API key", type="password")

if api_key:
    # Configure the Gemini Pro API
    genai.configure(api_key=api_key)

    # Upload an image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        # Generate CSV from image
        if st.button("Convert Image to CSV"):
            try:
                # Create a prompt for the model
                prompt = "Extract table data from the uploaded image and convert it to CSV format."

                # Convert image to text (assuming LayoutLLM-like functionality)
                response = genai.text_generation(prompt=prompt)  # Replace with actual image-to-text API logic
                csv_result = response.text

                # Simulate a file-like object for pandas
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

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter your API key to proceed.")
