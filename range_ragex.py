import re

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

# Example usage
text = "4.72inch/12cm E27 Socket 7.08inch/18cm AC 100-240V 60W Max Wattage 7.48inch/19cm BULBS ARE NOT INCLUDED"
extracted_info = extract_info(text)

# Print the results
for entity, values in extracted_info.items():
    if isinstance(values, list):
        print(f"{entity.capitalize()}: {values}")
    else:
        print(f"{entity.capitalize()}: {values}")
