import easyocr
import cv2
import os
import re
import csv
import pandas as pd

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to extract information using regex
def extract_info(text):
    # Define patterns for each entity, including both long and short forms
    patterns = {
        'weight': r'(\d+\.?\d*)\s?(g|kg|microgram|mg|milligram|mcg|ounce|oz|pound|lb|ton|grams|kilogram|kilograms|milligrams|micrograms|pounds|tons)',
        'height': r'(\d+\.?\d*)\s?(cm|mm|m|ft|foot|inch|inches|metre|yard|yards|centimetre|millimetre|metre)',
        'width': r'(\d+\.?\d*)\s?(cm|mm|m|ft|foot|inch|inches|metre|yard|yards|centimetre|millimetre|metre)',
        'depth': r'(\d+\.?\d*)\s?(cm|mm|m|ft|foot|inch|inches|metre|yard|yards|centimetre|millimetre|metre)',
        'voltage': r'(\d+\.?\d*-\d+\.?\d*|\d+\.?\d*)\s?(v|kv|volt|volts|kilovolt|millivolt)',
        'wattage': r'(\d+\.?\d*)\s?(w|kw|watt|watts|kilowatt)',
        'volume': r'(\d+\.?\d*)\s?(ml|l|litre|litres|millilitre|millilitres|centilitre|cl|cubic foot|cubic inch|cup|decilitre|dl|fluid ounce|oz|gallon|imperial gallon|pint|quart)'
    }

    extracted_data = {}

    # Iterate over each entity and apply the pattern
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Parse range if it's present, otherwise treat as a single value
            extracted_values = []
            for match in matches:
                value = match[0]
                if '-' in value:  # Handle range (e.g., "100-240V")
                    start, end = value.split('-')
                    extracted_values.extend([float(start), float(end)])
                else:
                    extracted_values.append(float(value))
            # Sort the values
            sorted_values = sorted(extracted_values)
            extracted_data[key] = sorted_values
        else:
            extracted_data[key] = 'Not found'

    return extracted_data


# Function to process images in a directory and merge results with an input CSV
def process_images_and_merge(input_csv, directory_path, output_csv):
    # Load input CSV file
    df = pd.read_csv(input_csv)

    # Sort the CSV by 'image_link' column (assuming this column contains the image file names)
    df = df.sort_values(by='image_link')

    # Create lists to hold extracted information
    voltages, wattages, volumes = [], [], []

    # Sort and iterate through all image files in the directory
    fld_img = sorted(os.listdir(directory_path))

    for image_name in fld_img:
        image_path = os.path.join(directory_path, image_name)

        if os.path.isfile(image_path):
            print(f"Processing {image_name}...")

            # Perform text detection and extraction
            results = reader.readtext(image_path)

            # Combine all extracted text into a single string
            text_string = ' '.join([text for (bbox, text, prob) in results])

            # Extract information using regex
            extracted_info = extract_info(text_string)

            # Add extracted data to respective lists
            voltages.append(extracted_info.get('voltage', 'Not found'))
            wattages.append(extracted_info.get('wattage', 'Not found'))
            volumes.append(extracted_info.get('volume', 'Not found'))

        else:
            # If the image does not exist or cannot be processed, add "Not found"
            voltages.append('Not found')
            wattages.append('Not found')
            volumes.append('Not found')

    # Add new columns to the DataFrame
    df['Voltage'] = voltages
    df['Wattage'] = wattages
    df['Volume'] = volumes

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Extraction complete. Results saved in {output_csv}")

# Paths (modify these according to your file paths)
input_csv = '/content/filtered_1000_rows.csv'  # Replace with your input CSV file path
directory_path = '/content/drive/MyDrive/1000_V_W/1000_V_W'  # Replace with your image directory path
output_csv = '/content/output.csv'  # Replace with your output CSV file path

# Process the images, merge with the CSV, and save the result
process_images_and_merge(input_csv, directory_path, output_csv)
