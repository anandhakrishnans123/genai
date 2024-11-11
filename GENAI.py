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
        
        # Initialize session state to track image rotation
        if 'rotation_angle' not in st.session_state:
            st.session_state.rotation_angle = 0
        
        # Button to rotate the image by 90 degrees
        if st.button("Rotate Image 90°"):
            st.session_state.rotation_angle += 90
            st.session_state.rotation_angle %= 360  # Ensure angle stays within 0-359 degrees
        
        # Rotate the image and expand it to ensure full dimensions are kept
        rotated_img = img.rotate(st.session_state.rotation_angle, expand=True)
        st.image(rotated_img, caption='Uploaded Image (Rotated)', use_column_width=True)

        # Generate CSV from image
        if st.button("Convert Image to CSV"):
            try:
                # Create a prompt for the model
                prompt = "Extract data from the uploaded image, extract the data including handwritten text, numbers and convert it to a CSV format. If possible, identify the type of data (e.g., names, dates, numbers) and structure the CSV accordingly. Also only give out the output table no other specific information is required"
                # Pass the image and prompt to the model
                response = model.generate_content([prompt, rotated_img])  # Assuming this format works with your API
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

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter your API key to proceed.")
