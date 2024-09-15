import re

def process_units(input_list):
    # Extended unit mapping, all units are in singular form
    unit_mapping = {
        'v': 'volt',
        'kv': 'kilovolt',
        'mv': 'millivolt',
        'w': 'watt',
        'kw': 'kilowatt',
        'ml': 'millilitre',
        'l': 'litre',
        'cl': 'centilitre',
        'microlitre': 'microlitre',
        'cubic foot': 'cubic foot',
        'cubic inch': 'cubic inch',
        'cup': 'cup',
        'dl': 'decilitre',
        'fluid ounce': 'fluid ounce',
        'gallon': 'gallon',
        'imperial gallon': 'imperial gallon',
        'pint': 'pint',
        'quart': 'quart',
        'g': 'gram',
        'kg': 'kilogram',
        'mg': 'milligram',
        'mcg': 'microgram',
        'lb': 'pound',
        'oz': 'ounce',
        'ton': 'ton',
        'cm': 'centimetre',
        'mm': 'millimetre',
        'm': 'metre',
        'ft': 'foot',
        'inch': 'inch',
        'yard': 'yard'
    }

    # Extract and process the units from the input list
    values = []
    unit = None

    for item in input_list:
        # Use regex to extract numeric value and unit
        match = re.match(r'(\d+\.?\d*)\s*([a-zA-Z]+)', item)
        if match:
            value = float(match.group(1))
            current_unit = match.group(2).lower()

            if unit is None:
                unit = current_unit

            # Only add to list if the unit matches the first unit encountered
            if current_unit == unit:
                values.append(value)
    
    # Convert the unit to its full form
    full_unit = unit_mapping.get(unit, unit)
    
    # Sort values in ascending order
    values.sort()
    
    # Return the sorted list and the unit
    return values, full_unit
    
