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
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Upload an image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        # Generate CSV from image
        if st.button("Convert Image to CSV"):
            try:
                # Assuming the model takes image input directly
                response = model.generate_content(img)  # Replace with actual image-to-text API call if available
                csv_result = response.text

                # Preprocess the CSV result
                # Assuming the values are space-separated, modify as needed
                rows = csv_result.splitlines()  # Split rows
                rows = [row.split('|') for row in rows]  # Split columns by pipe '|' or other delimiter

                # Create a DataFrame manually if CSV format is incorrect
                df = pd.DataFrame(rows)

                # Save the DataFrame to a CSV file
                csv_file_path = 'csv_output.csv'
                df.to_csv(csv_file_path, index=False, header=False)  # Save without headers, modify if needed

                st.success(f"CSV file saved as {csv_file_path}")
                st.write(df)  # Display the DataFrame

                # Provide a download link
                with open(csv_file_path, "rb") as f:
                    st.download_button("Download CSV", f, file_name=csv_file_path)

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter your API key to proceed.")
