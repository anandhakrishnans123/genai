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

        if st.button("Convert Image to CSV"):
            try:
                # Improve prompt with specific data types
                prompt = "Extract data like names, dates, or numbers from the uploaded image and present it in a CSV format."
                # Pass the image and prompt to the model (check model documentation for response format)
                response = model.generate_content([prompt, img])

                # Access text data from the response (adjust based on model output format)
                if hasattr(response, 'get_text'):  # Assuming a get_text method exists
                    csv_result = response.get_text()  # Replace with appropriate method
                else:
                    st.error("Model response format is unexpected. Check documentation.")
                    continue

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
