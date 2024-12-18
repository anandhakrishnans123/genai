import streamlit as st
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF for PDF handling

st.title("PDF or Image to Text Extractor")

# Input for API key
api_key = "AIzaSyBA3sUF2AFbcYwrsuY7zVu38dB-pOA-v9c"

if api_key:
    # Configure the Gemini Pro API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Upload an image or a PDF
    uploaded_file = st.file_uploader("Upload an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

    # Debugging: Print the uploaded file type
    if uploaded_file is not None:
        st.write(f"Uploaded file type: {uploaded_file.type}")

        file_type = uploaded_file.type
        if file_type in ["image/png", "image/jpg", "image/jpeg"]:
            # Handle image files
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

            # Generate text from the image
            if st.button("Extract Text from Image"):
                try:
                    # Create a prompt for the model
                    prompt = "Extract the value of net payable amount, title of the image, name and address of the bill receiver, date of billing, due date, and circle name from the image"
                    response = model.generate_content([prompt, rotated_img])  # Assuming this format works with your API
                    
                    # Print the response from the API
                    st.write(response.text)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

        elif file_type == "application/pdf":
            # Handle PDF files
            doc = fitz.open(uploaded_file)
            full_text = ""
            
            # Extract text from each page
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                full_text += page.get_text()

            st.write("Extracted Text from PDF:")
            st.text_area("PDF Content", full_text, height=300)

            # Generate content from the PDF text
            if st.button("Generate Content from PDF"):
                try:
                    # Create a prompt for the model
                    prompt = "Summarize the content of this PDF and extract key information."
                    response = model.generate_content([prompt, full_text])  # Assuming this format works with your API
                    
                    # Print the response from the API
                    st.write(response.text)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

else:
    st.warning("Please enter your API key to proceed.")
