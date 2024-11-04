import streamlit as st
import pandas as pd
from io import StringIO
from PIL import Image
import layoutparser as lp  # Make sure to install layoutparser

st.title("Image to CSV Converter")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    if st.button("Convert Image to CSV"):
        try:
            # Extract text from image using OCR (Tesseract or similar)
            ocr_agent = lp.TesseractAgent(languages='eng')
            ocr_result = ocr_agent.detect(img)

            # Convert the detected text into a CSV-compatible format
            extracted_text = ocr_result.get_text()
            
            # Simulate CSV format if necessary
            data_io = StringIO(extracted_text)
            
            # Read into DataFrame, assuming CSV formatting
            df = pd.read_csv(data_io, sep=',')  # Adjust separator if needed

            csv_file_path = 'csv_output.csv'
            df.to_csv(csv_file_path, index=False)

            st.success(f"CSV file saved as {csv_file_path}")
            st.write(df)  # Display the DataFrame

            # Provide a download link
            with open(csv_file_path, "rb") as f:
                st.download_button("Download CSV", f, file_name='output.csv')

        except Exception as e:
            st.error(f"An error occurred: {e}")
