# © 2025 B.A.D. Black Apex Development LLC
# All rights reserved.
# This software and its associated name, logo, and branding are the intellectual property of
# B.A.D. Black Apex Development LLC — registered in the State of Ohio (Entity #5448030).
# Unauthorized use, reproduction, or distribution is prohibited and may violate
# copyright, trademark, and unfair competition laws.


# -----------------------------------------------------------------------------------------
from dearpygui import dearpygui as dpg
import bcrypt
import hashlib
import logging
import json
import os
import Control

# -----------------------------------------------------------------------------------------
dpg.create_context()

# -----------------------------------------------------------------------------------------
# Deletes previous log file and creates a new one.
def _initiate_log_file():
    filename = "app.log"
    if os.path.exists(filename):
        os.remove(filename)
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

# -----------------------------------------------------------------------------------------
# Saves a gear name to a JSON list if it doesn't already exist.
def save_deployment_gear(gear_name, username: str):
    deployment_gear_file = f"{username}_deployment_gear.json"

    #Load existing data or create new data
    if os.path.exists(deployment_gear_file):
        try:
            with open(deployment_gear_file, 'r') as f:
                data_for_deployment_gear = json.load(f)
            if not isinstance(data_for_deployment_gear, list):
                print(f"[Error] Data in {deployment_gear_file} is not a list.")
                return
        except json.JSONDecodeError:
            print(f"[Error] Failed to decode JSON in {deployment_gear_file}.")
            return
    #Create new list data
    else:
        data_for_deployment_gear = []

    #Check for existence
    if gear_name not in data_for_deployment_gear:
        data_for_deployment_gear.append(gear_name)

        #Save updated list back to file
        with open(deployment_gear_file, 'w') as f:
            json.dump(data_for_deployment_gear, f, indent=4)

# -----------------------------------------------------------------------------------------
# Loads and returns a list of gear names from a JSON file. Returns None if file missing or empty.
def load_deployment_gear(username: str):
    filename = f"{username}_deployment_gear.json"

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

# -----------------------------------------------------------------------------------------
# Deletes a specific gear entry from a JSON list file.
def delete_deployment_gear(gear_name, username: str):
    filename = f"{username}_deployment_gear.json"

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

# -----------------------------------------------------------------------------------------
def save_deployment_gear_score(score: int, gear_name: str, username: str):
    filename = f"{username}_deployment_scores.json"
    # Step 1: Load existing data (or create empty structure if file doesn't exist)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Step 2: Append to the list for the given gear_name
    if gear_name not in data:
        data[gear_name] = []

    data[gear_name].append(score)

    # Step 3: Write the updated data back to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------------------------------------------------------------------
def delete_deployment_gear_scores(gear_name, username: str):
    filename = f"{username}_deployment_times.json"

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

# -----------------------------------------------------------------------------------------
def _get_sorted_deployment_scores(key_name: str, username: str) -> list:
    filename = f"{username}_deployment_scores.json"

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
        with open(filename, 'r') as file:
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

# -----------------------------------------------------------------------------------------
def create_user_data_files(sender, app_data, user_data):
    username = dpg.get_value(user_data[1])
    password = dpg.get_value(user_data[2])
    account_database_file = "account_database"

    #Read in or create account database file
    if os.path.exists(account_database_file):
        with open(account_database_file, "r") as f:
            data_for_accounts = json.load(f)
    else:
        data_for_accounts = {}

    #Hash user data
    salt = bcrypt.gensalt()
    hashed_and_salted_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    hashed_username = hashlib.sha256(username.encode("utf-8")).hexdigest()

    #Checks if username already exists.
    if hashed_username in data_for_accounts:
        return "Already exists"

    #Create user
    data_for_accounts[hashed_username] = []

    #Append password to corresponding user
    data_for_accounts[hashed_username].append(hashed_and_salted_password)

    #Append user to account database file
    with open(account_database_file, "w") as f:
        json.dump(data_for_accounts, f, indent=4)

    return "Creation Successful"

# -----------------------------------------------------------------------------------------
def _delete_user_data_files(sender, app_data, user_data):
    username = dpg.get_value(user_data[1])
    account_database_file = "account_database"

    #Read in or create account database file
    if os.path.exists(account_database_file):
        with open(account_database_file, "r") as f:
            data_for_accounts = json.load(f)
    else:
        return "Does not exist" #Because user doesn't exist if account database doesn't exist

    #Hash user data
    hashed_username = hashlib.sha256(username.encode("utf-8")).hexdigest()

    #Checks if username already exists.
    if hashed_username in data_for_accounts:
        del data_for_accounts[hashed_username]
        with open(account_database_file, "w") as f:
            json.dump(data_for_accounts, f, indent=4)
        deployment_gear_file = f"{username}_deployment_gear.json"
        deployment_gear_scores_file = f"{username}_deployment_gear_scores.json"
        try:
            os.remove(deployment_gear_file)
        except FileNotFoundError:
            logging.info(f"deployment gear file for user {username} not found")
        try:
            os.remove(deployment_gear_scores_file)
        except FileNotFoundError:
            logging.info(f"deployment gear times file for user {username} not found")
    else:
        return "Does not exist"

# -----------------------------------------------------------------------------------------
def _verify_user_password(sender, app_data, user_data):
    username = dpg.get_value(user_data[1])
    hashed_username = hashlib.sha256(username.encode("utf-8")).hexdigest()
    password = dpg.get_value(user_data[2])
    account_database_file = "account_database"

    # Read in or create account database file
    if os.path.exists(account_database_file):
        with open(account_database_file, "r") as f:
            data_for_accounts = json.load(f)
    else:
        return "User not in database"

    #check if user exists in database
    if hashed_username not in data_for_accounts:
        return "User not in database"

    #check password
    result = False
    if data_for_accounts is not None:
        password_of_hashed_username = data_for_accounts.get(hashed_username, ["<missing>"])[0]
        result = bcrypt.checkpw(password.encode("utf-8"), password_of_hashed_username.encode("utf-8"))
    return [username,result]

