import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO  # Import StringIO
from PIL import Image

st.title("Image to CSV Converter")

# Input for API key
api_key = "AIzaSyBA3sUF2AFbcYwrsuY7zVu38dB-pOA-v9c"

if api_key:
    # Configure the Gemini Pro API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Upload an image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        # Button to extract text from the image
        if st.button("Convert Image to Text"):
            try:
                # Create a prompt for extracting text
                text_prompt = "Extract text from the uploaded image."
                # Pass the image and prompt to the model
                text_response = model.generate_content([text_prompt, img])  # Check the actual method call if needed
                extracted_text = text_response.text

                # Display the extracted text
                st.subheader("Extracted Text")
                st.text(extracted_text)

            except Exception as e:
                st.error(f"An error occurred while extracting text: {e}")

        # Button to convert image to CSV
        if st.button("Convert Image to CSV"):
            try:
                # Create a prompt for the model
                csv_prompt = "Extract data from the uploaded image and convert it to CSV format."
                # Pass the image and prompt to the model
                csv_response = model.generate_content([csv_prompt, img])  # Check actual method call format
                csv_result = csv_response.text

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

            except Exception as e:
                st.error(f"An error occurred while converting to CSV: {e}")
else:
    st.warning("Please enter your API key to proceed.")
