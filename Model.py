import json
import os

#todo save this to a file of gear and every app load load those gear to fill gear list
def save_new_gear():
    print("new gear saved")

def save_deployment_time(time, gear_name, filename="deployment_scores.json"):
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


def delete_deployment_time(gear_name, filename="deployment_scores.json"):
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
        print(f"Deleted all deployment records for: {gear_name}")
    else:
        print(f"No records found for gear: {gear_name}")
        return

    # Step 4: Save updated data back to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_past_scores():
    #testing
    training_data = {1: 95, 2: 110, 3: 125}
    print("provide data to show on graph")

    #testing
    return training_data