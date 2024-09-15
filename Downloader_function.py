import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

# Initialize a global variable to track the current row index
current_row_index = 0

def download_image_from_csv(csv_file):
    """
    Downloads the next image from the CSV and removes the row after downloading.
    
    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        tuple: The downloaded image (PIL object) and the entity name (str).
    """
    global current_row_index
    try:
        # Load the CSV file into DataFrame (with backup if it's empty)
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            print(f"CSV file {csv_file} does not exist.")
            return None, None

        # Check if the row index is within the bounds of the DataFrame
        if current_row_index >= len(df):
            print("No more images to download.")
            return None, None

        # Select the row by current_row_index
        selected_row = df.iloc[current_row_index]

        # Extract image URL and entity name
        image_url = selected_row['image_link']
        entity_name = selected_row['entity_name']

        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise error if the HTTP request failed

        # Open the image using PIL
        image = Image.open(BytesIO(response.content))

        # Print for feedback (optional)
        print(f"Successfully downloaded image for {entity_name} from {image_url}")
        
        # Delete the row corresponding to the current_row_index
        df = df.drop(df.index[current_row_index])

        # Save the modified DataFrame back to the CSV file
        df.to_csv(csv_file, index=False)

        # You could also increment the row index only if deletion succeeds
        current_row_index += 1

        # Return the image object and entity name
        return image, entity_name

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")
        return None, None
    except IndexError:
        print(f"Row index out of bounds.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None


# Example usage:
csv_file_path = '/Users/ericvaish/Downloads/student_resource 3/dataset/test_copy.csv'

# Call the helper function multiple times
for _ in range(5):  # Simulate repeated calls
    image, entity_name = download_image_from_csv(csv_file_path)

    # Display the image and entity name if available
    if image and entity_name:
        image.show()  # This will open the image in a default image viewer
        print(f"Entity Name: {entity_name}")
    else:
        break  # Exit the loop if no more images
