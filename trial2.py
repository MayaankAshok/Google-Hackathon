import csv
from fuzzywuzzy import process
import fuzzywuzzy
import re

import fuzzywuzzy.fuzz

# List of generic terms to ignore
GENERIC_TERMS = {
    'tablet', 'syrup', 'capsule', 'injection', 'cream', 'gel', 'drops', 'spray',
    'mg', 'ml', 'gm', 'g', 'kg', 'l', 'iu', 'mcg', 'microgram', 'milligram', 'gram', 'kilogram', 'liter',
    'oral', 'topical', 'solution', 'suspension', 'powder', 'ointment', 'liquid', 'patch', 'inhaler'
}

def extract_drug_name(name):
    """
    Extract the meaningful drug name by removing generic terms and numbers.
    
    Args:
        name (str): The medicine name to process.
    
    Returns:
        str: The extracted drug name.
    """
    # Remove numbers and special characters
    name = re.sub(r'\d+', '', name)  # Remove numbers
    name = re.sub(r'[^\w\s]', '', name)  # Remove special characters
    
    # Split the name into words and filter out generic terms
    words = [word for word in name.lower().split() if word not in GENERIC_TERMS]
    return ' '.join(words)


def load_medicine_db(csv_file):
    """
    Load medicine database from a CSV file.
    
    Args:
        csv_file (str): Path to the CSV file containing medicine data.
    
    Returns:
        dict: A dictionary containing medicine data.
    """
    medicine_db = {}
    
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            print("CSV file opened successfully.")  # Debugging
            
            for row in reader:
                #print("Processing row:", row)  # Debugging
                # Extract the drug name
                key = extract_drug_name(row['name'])
                medicine_db[key] = {
                    'big_name': row['name'],
                    'name': extract_drug_name(row['name']),
                    'short_composition1': row['short_composition1'].split(', ') if row['short_composition1'] else [],
                    'short_composition2': row['short_composition2'].split(', ') if row['short_composition2'] else [],
                }
        
        print("Medicine database loaded successfully.")  # Debugging
        return medicine_db
    
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return {}
    except KeyError as e:
        print(f"Error: Missing expected column in CSV file: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


def verify_medicine(medicine_name, medicine_db, threshold=60, length_threshold=5):
    """
    Verify if a medicine exists in the database using fuzzy matching and length-based filtering.
    
    Args:
        medicine_name (str): Name of the medicine to verify.
        medicine_db (dict): Medicine database loaded from CSV.
        threshold (int): Minimum similarity score for a match (0-100).
        length_threshold (int): Maximum allowed length difference between input and matched name.
    
    Returns:
        dict: Verification result with status, info, or suggestions.
    """
    # Extract the drug name from the input medicine name
    processed_name = extract_drug_name(medicine_name)
    print(processed_name)
    
    # Use fuzzywuzzy to find the best match
    best_match, score = process.extractOne(processed_name, medicine_db.keys(), scorer= fuzzywuzzy.fuzz.ratio)
    
    # Calculate the length difference
    input_length = len(processed_name)
    match_length = len(best_match)
    length_difference = abs(input_length - match_length)
    
    # Check if the best match meets the thresholds
    if  score >= threshold and length_difference <= length_threshold:
        return {
            'status': 'found',
            'info': medicine_db[best_match],
            'match_score': score,  # Optional: Include the match score for debugging
            'length_difference': length_difference  # Optional: Include the length difference for debugging
        }
    else:
        return {
            'status': 'not found',
            'suggestions': []  # No suggestions for now
        }


# Load medicine database from CSV
medicine_db = load_medicine_db('data.csv')


# Test the function
test_medicine = 'Byplex fort'
verification_result = verify_medicine(test_medicine, medicine_db)
print(f"Verification result for {test_medicine}:")
print(verification_result)

"""test_medicine = 'Lanzol 15mg Capsule'
verification_result = verify_medicine(test_medicine, medicine_db)
print(f"Verification result for {test_medicine}:")
print(verification_result)

test_medicine = 'Stilbestrol 25mg tablet'
verification_result = verify_medicine(test_medicine, medicine_db)
print(f"Verification result for {test_medicine}:")
print(verification_result)"""