import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO
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

        # Generate CSV from image
        if st.button("Convert Image to CSV"):
            try:
                # Create a prompt for the model
                prompt = ("Extract data from the uploaded image, ensuring that every cell value is "
                           "accurately recognized and captured. Convert the extracted data into CSV format, "
                           "maintaining the original structure and layout of the data as presented in the image. "
                           "Include headers and ensure that any special characters or formatting are preserved in the CSV output.")

                # Pass the image and prompt to the model
                response = model.generate_content([prompt, img])
                csv_result = response.text

                # Log the CSV output for debugging
                st.text(csv_result)  # Use st.text for raw text display

                # Use StringIO to simulate a file-like object for pandas
                data_io = StringIO(csv_result)

                # Read the data into a DataFrame
                try:
                    df = pd.read_csv(data_io)
                except pd.errors.ParserError as parse_error:
                    st.error(f"CSV Parsing Error: {parse_error}")

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
