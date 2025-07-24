import json
import os

import json
import os

def save_deployment_gear(gear_name, filename="deployment_gear.json"):
    """Saves a gear name to a JSON list if it doesn't already exist."""

    gear_name = gear_name.strip()

    # Step 1: Load existing data or create new list
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            if not isinstance(data, list):
                print(f"[Error] Data in {filename} is not a list.")
                return
        except json.JSONDecodeError:
            print(f"[Error] Failed to decode JSON in {filename}.")
            return
    else:
        data = []

    # Step 2: Check for existence
    if gear_name not in data:
        data.append(gear_name)

        # Step 3: Save updated list back to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


def save_deployment_gear_time(time, gear_name, filename="deployment_scores.json"):
    # Step 1: Load existing data (or create empty structure if file doesn't exist)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Step 2: Append to the list for the given gear_name
    if gear_name not in data:
        data[gear_name] = []

    data[gear_name].append(time)

    # Step 3: Write the updated data back to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Score {time} saved for: {gear_name}")


def load_deployment_gear(filename="deployment_gear.json"):
    """Loads and returns a list of gear names from a JSON file. Returns None if file missing or empty."""
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            if isinstance(data, list) and data:
                return data
            else:
                return None
    except json.JSONDecodeError:
        print(f"[Error] Failed to decode JSON in: {filename}")
        return None


def delete_deployment_gear_time(gear_name, filename="deployment_scores.json"):
    # Step 1: Check if the file exists
    if not os.path.exists(filename):
        print("No data file found.")
        return

    # Step 2: Load the existing data
    with open(filename, "r") as f:
        data = json.load(f)

    # Step 3: Check if gear_name exists
    if gear_name in data:
        del data[gear_name]
    else:
        return

    # Step 4: Save updated data back to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def delete_deployment_gear(gear_name, filename="deployment_gear.json"):
    """Deletes a specific gear entry from a JSON list file."""

    # Check if the file exists
    if not os.path.exists(filename):
        print(f"[Error] File not found: {filename}")
        return

    # Load the existing JSON data
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"[Error] Failed to decode JSON in: {filename}")
        return

    # Ensure data is a list
    if not isinstance(data, list):
        print(f"[Error] Data in {filename} is not a valid list.")
        return

    # Attempt to remove the gear entry
    if gear_name in data:
        data.remove(gear_name)

        # Write the updated list back to the file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    else:
        print(f"[Warning] Gear '{gear_name}' not found in file.")


def get_past_scores():
    #testing
    training_data = {1: 95, 2: 110, 3: 125}
    print("provide data to show on graph")

    #testing
    return training_data