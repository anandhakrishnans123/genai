import streamlit as st
from PIL import Image, ExifTags
import numpy as np
import cv2
import pytesseract

# Ensure pytesseract is installed and configured correctly
# pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract'  # Uncomment and set the path if needed

def correct_image_orientation(image):
    """Corrects the orientation of an image using EXIF data or manual analysis."""
    try:
        # Check EXIF orientation data
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No EXIF data or issue reading it, move to manual check
        pass

    # Convert the image to a numpy array and analyze its orientation
    image_array = np.array(image)
    if image_array.shape[0] > image_array.shape[1]:  # Check if the image is in portrait mode
        image = image.rotate(90, expand=True)

    return image

def detect_text_orientation(image):
    """Detects and corrects the orientation using pytesseract."""
    orientation_data = pytesseract.image_to_osd(image)
    if "Rotate: 90" in orientation_data:
        image = image.rotate(270, expand=True)
    elif "Rotate: 180" in orientation_data:
        image = image.rotate(180, expand=True)
    elif "Rotate: 270" in orientation_data:
        image = image.rotate(90, expand=True)
    return image

st.title("Automated Image Orientation Correction")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    # Step 1: Correct orientation using EXIF data
    img = correct_image_orientation(img)

    # Step 2: Further analyze and correct using OCR if needed
    img = detect_text_orientation(img)

    st.image(img, caption='Corrected Image', use_column_width=True)
    st.success("Image orientation corrected!")
else:
    st.info("Please upload an image to proceed.")
