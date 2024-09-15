import cv2
import numpy as np
from PIL import Image
import easyocr

# Initialize the OCR reader (use your appropriate language setting, e.g., 'en' for English)
reader = easyocr.Reader(['en'])

# Preprocess the image
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding to convert the image to binary
    binary_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Resize image to make text clearer (if needed)
    resized_image = cv2.resize(binary_image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    
    return resized_image

# Function to convert OpenCV image to PIL Image
def convert_cv2_to_pil(cv2_img):
    pil_img = Image.fromarray(cv2_img)
    return pil_img

# Function to extract text from an image and return the entity value
def handle_voltage_wattage(image, entity_name):
    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(image)

        # Convert OpenCV image to PIL Image
        pil_image = convert_cv2_to_pil(preprocessed_image)

        # Perform text detection and extraction using the preprocessed image
        results = reader.readtext(np.array(pil_image))

        # Combine all extracted text into a single string
        text_string = ' '.join([text for (bbox, text, prob) in results])

        # Extract information using regex based on the entity_name
        extracted_value = extract_info(text_string, entity_name)
        return extracted_value
    except Exception as e:
        return f"Error processing the image: {e}"
