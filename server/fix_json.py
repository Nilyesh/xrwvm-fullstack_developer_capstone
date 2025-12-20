import json

# --- Configuration ---
INPUT_FILE = "database/data/dealerships.json"
OUTPUT_FILE = "database/data/dealerships_fixed.json"
# Match your app name and model name (lowercase)
MODEL_NAME = "djangoapp.dealer"
# ---------------------


def transform_fixture(input_path, output_path, model_name):
    with open(input_path, "r") as f:
        data = json.load(f)

    dealers = data
    transformed_data = []

    for dealer in dealers:
        new_dealer_obj = {"model": model_name, "pk": dealer.pop("id"), "fields": dealer}
        transformed_data.append(new_dealer_obj)

    with open(output_path, "w") as f_out:
        json.dump(transformed_data, f_out, indent=4)
