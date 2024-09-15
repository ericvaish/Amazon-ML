import easyocr
import os
import re
import pandas as pd

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to extract information using regex
def extract_info(text, entity_name):
    # Define patterns for each entity with capturing groups for value and unit
    patterns = {
        'weight': r'(\d+\.?\d*)\s?(g|kg|microgram|mg|milligram|mcg|ounce|oz|pound|lb|ton|grams|kilogram|kilograms|milligrams|micrograms|pounds|tons)',
        'height': r'(\d+\.?\d*)\s?(cm|mm|m|ft|foot|inch|inches|metre|yard|yards|centimetre|millimetre|metre|")',
        'width': r'(\d+\.?\d*)\s?(cm|mm|m|ft|foot|inch|inches|metre|yard|yards|centimetre|millimetre|metre|")',
        'depth': r'(\d+\.?\d*)\s?(cm|mm|m|ft|foot|inch|inches|metre|yard|yards|centimetre|millimetre|metre|")',
        'voltage': r'(\d+\.?\d*-\d+\.?\d*|\d+\.?\d*)\s?(v|kv|volt|volts|kilovolt|millivolt)',
        'wattage': r'(\d+\.?\d*)\s?(w|kw|watt|watts|kilowatt)',
        'volume': r'(\d+\.?\d*)\s?(ml|l|litre|litres|millilitre|millilitres|centilitre|cl|cubic foot|cubic inch|cup|decilitre|dl|fluid ounce|oz|gallon|imperial gallon|pint|quart)'
    }

    extracted_data = {}

    # Get the pattern for the specific entity_name
    pattern = patterns.get(entity_name.lower())
    
    if pattern:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Format the extracted values with units
            extracted_values = [f"{match[0]} {match[1]}" for match in matches]
            extracted_data[entity_name] = extracted_values
        else:
            extracted_data[entity_name] = 'Not found'
    else:
        extracted_data[entity_name] = 'Pattern not defined'

    return extracted_data

# Function to process images in a directory and merge results with an input CSV
def process_images_and_merge(input_csv, directory_path, output_csv):
    # Load input CSV file
    df = pd.read_csv(input_csv)

    # Create a list to hold extracted information
    data = []

    # Iterate through each row in the CSV
    for index, row in df.iterrows():
        image_link = row['image_link']
        
        # Extract image name from the URL
        image_name = image_link.rsplit('/', 1)[-1].rsplit('.jpg', 1)[0] + '.jpg'
        entity_name = row['entity_name']
        
        # Construct image path
        image_path = os.path.join(directory_path, image_name)

        if os.path.isfile(image_path):
            print(f"Processing {image_name}...")

            # Perform text detection and extraction
            results = reader.readtext(image_path)

            # Combine all extracted text into a single string
            text_string = ' '.join([text for (bbox, text, prob) in results])

            # Extract information using regex based on the entity_name for the current row
            extracted_info = extract_info(text_string, entity_name)
            print(extracted_info)

            # Append the extracted info along with other row data
            row_data = row.to_dict()
            row_data.update(extracted_info)
            data.append(row_data)
        else:
            print(f"Image {image_name} not found.")

    # Create a DataFrame from the extracted data
    extracted_df = pd.DataFrame(data)

    # Save the updated CSV with the merged data
    extracted_df.to_csv(output_csv, index=False)

# Paths
input_csv = '/content/filtered_10_rows.csv'  # Replace with your input CSV file
directory_path = '/content/drive/MyDrive/10_img/10_img'  # Replace with your directory path
output_csv = '/content/merged_results.csv'  # Replace with your desired output CSV file

# Process the images, merge with the CSV, and save the result
process_images_and_merge(input_csv, directory_path, output_csv)
