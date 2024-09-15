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

    # Use regex to extract the numeric value and unit, including optional space and the " symbol
    match = re.match(r'(\d+\.?\d*)\s*([a-zA-Z"]+)', input_string)
    
    if match:
        value = match.group(1)
        unit = match.group(2).lower()

        # Find the singular form of the unit, if available
        full_unit = unit_mapping.get(unit, unit)

        # Return the expanded result with singular unit form
        return f"{value} {full_unit}"
    else:
        return "Invalid input"
