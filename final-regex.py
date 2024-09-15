import re

def expand_units(input_string):
    # Extended unit mapping from entity_unit_map, all units are in singular form
    unit_mapping = {
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
        'yard': 'yard',
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
        '"': 'inch'
    }

    # Use regex to find all occurrences of numeric values followed by units
    pattern = r'(\d+\.?\d*)\s*([a-zA-Z"]+)'
    matches = re.findall(pattern, input_string)
    
    if matches:
        expanded_results = []
        for match in matches:
            value = match[0]
            unit = match[1].lower()

            # Find the singular form of the unit, if available
            full_unit = unit_mapping.get(unit, unit)

            # Append the expanded result with singular unit form
            expanded_results.append(f"{value} {full_unit}")
        
        # Return the expanded results as a single string
        return ', '.join(expanded_results)
    else:
        return "No valid entities found"
