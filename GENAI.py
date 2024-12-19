import streamlit as st
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF for PDF handling
import io  # To handle in-memory file stream
from io import StringIO
import pandas as pd
from datetime import datetime

# Set up the Streamlit app title
st.title("PDF or Image to Text Extractor")

# Input for API key
api_key = "AIzaSyBA3sUF2AFbcYwrsuY7zVu38dB-pOA-v9c"  # Replace with your API key

if api_key:
    # Configure the Gemini Pro API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Upload an image or a PDF
    uploaded_file = st.file_uploader("Upload an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file is not None:
        # Debugging: Print the uploaded file type
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
                    prompt = ("Extract the value of net payable amount, title of the image, name and address of the bill receiver, "
                              "date of billing, due date, and circle name from the image.")
                    response = model.generate_content([prompt, rotated_img])  # Assuming this format works with your API
                    st.write(response.txt)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

        elif file_type == "application/pdf":
            # Handle PDF files
            pdf_data = uploaded_file.read()  # Read the uploaded file as bytes
            doc = fitz.open("pdf", pdf_data)  # Open the PDF using the correct format for bytes
            full_text = ""
            
            # Extract text from each page
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                full_text += page.get_text()

            # Generate content from the PDF text
            if st.button("Generate Content from PDF"):
                try:
                    # Create a prompt for the model
                    prompt = ("Extract the following details from the document and return them in a clean CSV format: "
                              "net payable amount, title, name and address of the bill receiver, date of billing, due date,Total energy consumed in KWH ,"
                              "and circle name. Ensure each field is in a separate column with appropriate headers, and return "
                              "'null' for any missing or unclear data. The CSV should be formatted correctly with commas as delimiters "
                              "and no extra spaces or errors.")
                    response = model.generate_content([prompt, full_text])

                    # Debugging: Inspect raw response
                    csv_result = response.text
                    st.write("Raw Response from API:")
                    st.write(csv_result)
                    
                    # Clean and parse CSV
                    # Strip leading/trailing whitespace
                    csv_result = csv_result.strip()
                    
                    # Check if the result starts with 'csv' and remove any non-CSV content
                    if csv_result.lower().startswith("csv"):
                        # If 'csv' is at the start, remove the first line or prefix before the actual data
                        csv_result = csv_result.split("\n", 1)[-1]  # Remove the first line (metadata/description)
                    
                    # Further clean up: remove any extra text that might appear after CSV content
                    lines = csv_result.split("\n")
                    valid_csv = "\n".join(line for line in lines if ',' in line)  # Only keep lines with commas (CSV rows)
                    
                    # Now, read the cleaned CSV content
                    data_io = StringIO(valid_csv)
                    df = pd.read_csv(data_io)
                    
                    # Save the cleaned DataFrame
                    csv_file_path = 'csv_output.csv'
                    df.to_csv(csv_file_path, index=False)
                    
                    st.success(f"CSV file saved as {csv_file_path}")
                    st.write("Generated DataFrame:")
                    st.write(df)

                    columns = [
                        'Res_Date', 'Department', 'Facility', 'Start Date', 'End Date', 
                        'Country', 'City', 'Activity', 'Activity Unit', 'Energy Type', 
                        'Energy Unit', 'Energy Consumption', 'Cost', 'Price p/u', 'CF Standard', 'Gas'
                    ]

                    # Create an empty DataFrame with the specified columns
                    df2 = pd.DataFrame(columns=columns)
                    # Add values from the original DataFrame
                    df2['Cost'] = df['net payable amount']
                    df2['End Date'] = df['due date']
                    df2['Start Date'] = df['date of billing']
                    df2['Facility'] = df['name and address of the bill receiver']
                    df2['City'] = df['circle name']
                    df2['Res_Date'] = datetime.now().strftime('%Y-%m-%d')
                    df2["Energy Unit"] = "KWh"
                    df2['CF Standard'] = "IMO"
                    df2['Gas'] = "CO2"
                    df2['Country'] = "India"
                    df2['Energy Type'] = "India"
                    df2["Energy Consumption"] = df["Total energy consumed in KWH"]
                    df2['End Date'] = pd.to_datetime(df2['End Date'], dayfirst=True)
                    df2['Start Date'] = pd.to_datetime(df2['Start Date'], dayfirst=True)
                    df2['Res_Date'] = pd.to_datetime(df2['Res_Date'], dayfirst=True)

                    # Create an in-memory Excel file
                    excel_buffer = io.BytesIO()
                    df2.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)  # Move the pointer to the start of the buffer

                    # Download button for Excel
                    st.download_button(
                        label="Download Excel",
                        data=excel_buffer,
                        file_name="downloaded_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                

else:
    st.warning("Please enter your API key to proceed.")
st.markdown(
    '<a href="https://samesg.samcorporate.com/app/oecs1clayjeh02r4azwfozndif0/page/default/data-upload/etl/emission-calculations/66545e850b4e5b2af3c80e81/list/create" target="_blank">'
    '<button>Upload to system</button></a>', 
    unsafe_allow_html=True
)
