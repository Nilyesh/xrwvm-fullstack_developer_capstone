import json
import os

# --- Configuration ---
INPUT_FILE = "database/data/dealerships.json"
OUTPUT_FILE = "database/data/dealerships_fixed.json"
MODEL_NAME = "djangoapp.dealer" # Match your app name and model name (lowercase)
# ---------------------

def transform_fixture(input_path, output_path, model_name):
    """Reads the JSON, transforms each object into Django fixture format, and saves it."""
    
    # 1. Load the original data
    with open(input_path, 'r') as f:
        data = json.load(f)

    # The original data is an object: {"dealerships": [ ... ]}
    # We only want the array inside the "dealerships" key.
    dealers = data
    
    transformed_data = []
    
    # 2. Iterate and transform each dealer object
    for dealer in dealers:
        # Create the new Django-compliant object structure
        new_dealer_obj = {
            "model": model_name,
            "pk": dealer.pop("id"),  # Use 'id' as the primary key and remove it from the fields
            "fields": {}
        }
        
        # Mapping the custom keys to Django Model keys (based on your model)
        new_dealer_obj["fields"] = {
            "name": dealer.get("full_name"),
            "city": dealer.get("city"),
            "state": dealer.get("st"),         # Use 'st' for the state abbreviation
            "address": dealer.get("address"),
            "zip_code": dealer.get("zip"),     # Use 'zip' for the zip_code field
            # NOTE: We intentionally OMIT the 'lat' and 'long' fields to avoid the error.
            # NOTE: If your Dealer model requires a 'phone' field, you must add it here or in the JSON.
            # "phone": "555-555-5555", # Example if phone is required and missing in JSON
        }
        
        transformed_data.append(new_dealer_obj)

    # 3. Save the correctly formatted fixture
    with open(output_path, 'w') as f:
        json.dump(transformed_data, f, indent=2)

    print(f"✅ Successfully transformed {len(transformed_data)} dealer objects.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    # Ensure the script runs from the 'server' directory
    transform_fixture(INPUT_FILE, OUTPUT_FILE, MODEL_NAME)