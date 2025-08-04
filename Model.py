import json
import os
from dearpygui import dearpygui as dpg
import json
import os
import Control

dpg.create_context()


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


def get_sorted_times_by_key(key_name: str, file_path: str = "deployment_scores.json") -> list:
    def time_to_milliseconds(time_str):
        hours, minutes, rest = time_str.split(':')
        seconds, millis = rest.split('.')
        total_millis = (
            int(hours) * 3600000 +
            int(minutes) * 60000 +
            int(seconds) * 1000 +
            int(millis)
        )
        return total_millis

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return []

    if key_name not in data:
        popup_tag = "not_found_popup"

        Control._check_window_exists(popup_tag)

        with dpg.window(label="Error", modal=True, tag=popup_tag, width=300, height=120, no_resize=True, pos=(200, 200)):
            dpg.add_text("No data to graph")
            dpg.add_spacing(count=2)
            dpg.add_button(label="OK", width=75, callback=lambda: Control._delete_window(popup_tag))

        return []

    time_list = data[key_name]
    result = []

    for t in time_list:
        if isinstance(t, str) and t.strip().lower() == "eightysix":
            result.append({"original": t, "milliseconds": "EightySix"})
        else:
            try:
                ms = time_to_milliseconds(t)
                result.append({"original": t, "milliseconds": ms})
            except Exception as e:
                print(f"Skipping malformed time '{t}': {e}")

    return result


