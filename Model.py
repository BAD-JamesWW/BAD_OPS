# © 2025 B.A.D. Black Apex Development LLC
# All rights reserved.
# This software and its associated name, logo, and branding are the intellectual property of
# B.A.D. Black Apex Development LLC — registered in the State of Ohio (Entity #5448030).
# Unauthorized use, reproduction, or distribution is prohibited and may violate
# copyright, trademark, and unfair competition laws.


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

    #Load existing data and verify it's a list.
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
    #Create new list data
    else:
        data = []

    #Saves new gear if it doesn't already exist.
    if gear_name not in data:
        data.append(gear_name)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


def save_deployment_gear_time(time, gear_name, filename="deployment_scores.json"):
    # Load existing data and verify it's a dict.
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                print(f"[Error] Data in {filename} is not a dict.")
                return
        except json.JSONDecodeError:
            print(f"[Error] Failed to decode JSON in {filename}.")
            return
    #the scores file will be a dict of lists, so times can be easily attached to gear
    else:
        data = {}

    #In case the scores file doesn't have the gear in its dict
    if gear_name not in data:
        data[gear_name] = []

    #Append new list data, to the dict key of gear_name
    data[gear_name].append(time)

    #Update file data
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)



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
    #Check if the file exists
    if not os.path.exists(filename):
        print("No data file found.")
        return

    #Load the existing data file
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"[Error] Data in {filename} is not a dict.")
            return
    except json.JSONDecodeError:
        print(f"[Error] Failed to decode JSON in {filename}.")
        return

    #Delete chosen gear in data file
    if gear_name in data:
        del data[gear_name]
    else:
        return

    #Update data file
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
    #Nested func. to convert time to ms.
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

    #Attempt to load data file & return empty list of fail.
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return []

    #Display popups and return empty list if corresponding gear time doesn't exist
    if key_name not in data:
        popup_tag = "not_found_popup"

        Control._check_window_exists(popup_tag)

        with dpg.window(label="Error", modal=True, tag=popup_tag, width=300, height=120, no_resize=True, pos=(200, 200)):
            dpg.add_text("No data to graph")
            dpg.add_spacing(count=2)
            dpg.add_button(label="OK", width=75, callback=lambda: Control._delete_window(popup_tag))

        return []

    # Format a list of times for corresponding gear and return it
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


