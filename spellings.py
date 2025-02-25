import csv

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
                # Extract the first word from the 'name' column
                first_word = row['name'].split()[0].lower()
                medicine_db[first_word] = {
                    'name': row['name'],
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


def verify_medicine(medicine_name, medicine_db):
    """
    Verify if a medicine exists in the database and return its details or suggestions.
    
    Args:
        medicine_name (str): Name of the medicine to verify.
        medicine_db (dict): Medicine database loaded from CSV.
    
    Returns:
        dict: Verification result with status, info, or suggestions.
    """
    # Extract the first word from the input medicine name
    first_word = medicine_name.split()[0].lower().strip()
    
    if first_word in medicine_db:
        return {
            'status': 'found',
            'info': medicine_db[first_word]
        }
    else:
        return {
            'status': 'not found',  # Explicitly return 'not found'
            'suggestions': []  # No suggestions for now
        }


# Load medicine database from CSV
medicine_db = load_medicine_db('data.csv')
print("Medicine database:", medicine_db)  # Debugging

# Test the function with a valid medicine name
"""test_medicine = 'Zyvocol 1% Dusting Powder'
verification_result = verify_medicine(test_medicine, medicine_db)
print(f"Verification result for {test_medicine}:")
print(verification_result)"""

# Test the function with a non-existent medicine name
test_medicine = 'Byplex fort'
verification_result = verify_medicine(test_medicine, medicine_db)
print(f"Verification result for {test_medicine}:")
print(verification_result)