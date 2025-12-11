# © 2025 B.A.D. Black Apex Development LLC
# All rights reserved.
# This software and its associated name, logo, and branding are the intellectual property of
# B.A.D. Black Apex Development LLC — registered in the State of Ohio (Entity #5448030).
# Unauthorized use, reproduction, or distribution is prohibited and may violate
# copyright, trademark, and unfair competition laws.


#Description: Responsible for controlling the flow of the program.

# -----------------------------------------------------------------------------------------
import View_HomeUI
import View_GearUI_TrainingOptions
import Model
import View_GearUI_TrainingOptions_Train
import dearpygui.dearpygui as dpg
import pygame
import os

# -----------------------------------------------------------------------------------------
pygame.mixer.init()

# -----------------------------------------------------------------------------------------
gears = dict()
is_user_logged_in = False
username_of_user_logged_in = ""

#-----------------------------------------------------------------------------------------
def main():
    Model._initiate_log_file() #So log file is created overwritten anew, to prevent bloating
    View_HomeUI._run_home_ui()
    View_HomeUI._create_homeUI()

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------------------
def play_sound(filename, wait=True):
    path = os.path.abspath(filename)
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        print(f"[Sound Error] File missing or empty: {path}")
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        if wait:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)
    except Exception as e:
        print("Audio playback failed:", e)

# -----------------------------------------------------------------------------------------
def _show_window(previous_window_tag):
    dpg.show_item(previous_window_tag)

# -----------------------------------------------------------------------------------------
def _hide_window(previous_window_tag):
    dpg.hide_item(previous_window_tag)

# -----------------------------------------------------------------------------------------
def _delete_window(window_tag):
    dpg.delete_item(window_tag)

# -----------------------------------------------------------------------------------------
def _check_window_exists(window_tag):
    if dpg.does_item_exist(window_tag):
        dpg.delete_item(window_tag)

# -----------------------------------------------------------------------------------------
def _start_training_options_window(sender, appdata, user_data):
    View_GearUI_TrainingOptions.start(sender, appdata, user_data)

# -----------------------------------------------------------------------------------------
def _show_training_options_train_window(sender, appdata, user_data):
    global is_user_logged_in, username_of_user_logged_in

    if is_user_logged_in is True and username_of_user_logged_in != "":
        View_GearUI_TrainingOptions_Train.show_timer(sender, appdata, user_data)
    else:
        View_GearUI_TrainingOptions._popup_generic_message("User must be logged in to train \ndeployment speed.")

# -----------------------------------------------------------------------------------------
def _add_gear(gear_name: str, input_tag: str):
    global is_user_logged_in, username_of_user_logged_in
    View_HomeUI.inputInProgress = False

    if not gear_name:
        View_HomeUI._popup_add_gear_failed(isInputEmpty=True)
        dpg.set_value(input_tag, "")
        return

    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    # theme
    with dpg.theme() as red_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))

    if gears.get(gear_name, "doesNotExist") == "doesNotExist":
        gears[gear_name] = {"gear_button_tag": gear_name}
        with dpg.group(horizontal=True, parent="button_container_home_ui"):
            dpg.add_spacer(width=padding)
            dpg.add_button(
                label=gear_name,
                width=button_width,
                height=100,
                tag=gear_name,
                callback=View_GearUI_TrainingOptions.start,
                user_data=[gear_name, "home_ui_parent_window"]
            )
            dpg.bind_item_theme(gear_name, red_button_theme)

        if is_user_logged_in and username_of_user_logged_in:
            Model.save_deployment_gear(gear_name=gear_name, username=username_of_user_logged_in)

        dpg.hide_item(input_tag)
        dpg.set_value(input_tag, "")
    else:
        View_HomeUI._popup_add_gear_failed(isInputEmpty=False)
        dpg.set_value(input_tag, "")

# -----------------------------------------------------------------------------------------
def _remove_gear(sender, app_data, user_data):
    global is_user_logged_in, username_of_user_logged_in
    View_HomeUI.inputInProgress = False
    input_tag = user_data[1]
    if dpg.is_item_shown(input_tag):
        gear_name = dpg.get_value(input_tag)
        if gear_name and gears.get(str(gear_name), "doesNotExist") != "doesNotExist":
            gearButtonToRemove = gears.pop(str(gear_name))
            dpg.delete_item(gearButtonToRemove["gear_button_tag"])

            # If a user is logged in, gear data can be deleted from their corresponding file
            if is_user_logged_in == True and username_of_user_logged_in != "":
                Model.delete_deployment_gear_scores(gear_name = gearButtonToRemove["gear_button_tag"], username = username_of_user_logged_in)
                Model.delete_deployment_gear(gear_name = gearButtonToRemove["gear_button_tag"], username = username_of_user_logged_in)

            dpg.hide_item(input_tag)
            dpg.set_value(input_tag, "")
        else:
            View_HomeUI._popup_remove_gear_failed(isInputEmpty=(gear_name == ""))
            dpg.set_value(input_tag, "")
    else:
        dpg.show_item(input_tag)

# -----------------------------------------------------------------------------------------
def _nuke_gear():
    global is_user_logged_in, username_of_user_logged_in
    if dpg.does_item_exist("nuke_confirm_window"):
        dpg.delete_item("nuke_confirm_window")

    play_sound("assets/audio/ui_sound_03.wav", wait=False)

    def _confirm():
        dpg.delete_item("nuke_confirm_window")
        for gear in list(gears):
            gearButtonToRemove = gears.pop(str(gear))
            dpg.delete_item(gearButtonToRemove["gear_button_tag"])

            # If a user is logged in, gear data can be deleted from their corresponding file
            if is_user_logged_in == True and username_of_user_logged_in != "":
                Model.delete_deployment_gear(gear_name = gearButtonToRemove["gear_button_tag"], username = username_of_user_logged_in)
                Model.delete_deployment_gear_scores(gear_name = gearButtonToRemove["gear_button_tag"], username = username_of_user_logged_in)

    def _cancel():
        dpg.delete_item("nuke_confirm_window")

    with dpg.window(label="Confirm Nuke", modal=True, tag="nuke_confirm_window", no_title_bar=True, width=360, height=150, pos=(300, 300)):
        dpg.add_text("Are you sure you want to nuke all gear?\nThis action cannot be undone.", wrap=330)
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Yes", width=75, callback=_confirm)
            dpg.add_button(label="No", width=75, callback=_cancel)

# -----------------------------------------------------------------------------------------
def _save_deployment_gear_score(score: int, gear_name: str):
    Model.save_deployment_gear_score(score = score, gear_name = gear_name, username = username_of_user_logged_in)

# -----------------------------------------------------------------------------------------
def get_sorted_deployment_scores(key_name: str) -> list:
    global is_user_logged_in, username_of_user_logged_in

    if is_user_logged_in == False and username_of_user_logged_in == "":
        View_GearUI_TrainingOptions._popup_generic_message("User must be logged in to get deployment \nscores.")
        return []

    if len(Model._get_sorted_deployment_scores(key_name, username_of_user_logged_in)) == 0:
        View_GearUI_TrainingOptions._popup_generic_message("No scores available.")

    return Model._get_sorted_deployment_scores(key_name, username_of_user_logged_in)

# -----------------------------------------------------------------------------------------
def _logout_user():
    global is_user_logged_in, username_of_user_logged_in

    if is_user_logged_in == True and username_of_user_logged_in != "":
        #reset global trackers
        is_user_logged_in = False
        username_of_user_logged_in = ""

        #Remove gear buttons from home UI
        View_HomeUI._clear_gear_buttons()

        # delete corresponding dpg items in memory, this is safe because user is logging out and won't care if their gear UI is removed.
        for gear in list(gears):
            gearButtonToRemove = gears.pop(str(gear))
            dpg.delete_item(gearButtonToRemove["gear_button_tag"])

        #Change header text of HomeUI
        dpg.set_value("homescreen_header_text", "Gear")
    else:
        return

# -----------------------------------------------------------------------------------------
def _create_user_data(sender, app_data, user_data):
    global is_user_logged_in, username_of_user_logged_in

    if is_user_logged_in == True and username_of_user_logged_in != "":
        View_HomeUI._popup_generic_message("You must be logged out to create \nan account")
        return

    #So user cannot create a username or password with an empty string
    if dpg.get_value(user_data[1]) == "":
        View_HomeUI._popup_generic_message("You cannot create an empty username")
        return
    if (dpg.get_value(user_data[2]) == "") or (" " in dpg.get_value(user_data[2])):
        View_HomeUI._popup_generic_message("Spaces in the password are prohibited")
        return

    #So user knows program is busy
    View_HomeUI._popup_busy_creating_user(sender, app_data, user_data)

    result =  Model.create_user_data_files(sender, app_data, user_data)

    #So busy popup goes away
    _check_window_exists(View_HomeUI.BUSY_CREATING_USER_WINDOW_TAG)

    # Yield one frame so DPG clears the modal stack, or next popup in this function bugs out and doesn't show
    dpg.split_frame()

    # Show popup if the username already exists
    if result == "Already exists":
        View_HomeUI._popup_create_user_failed(sender, app_data, user_data)
    elif result == "Creation Successful":
        View_HomeUI._popup_user_creation_result(dpg.get_value(user_data[1]))

# -----------------------------------------------------------------------------------------
def _delete_user_data(sender, app_data, user_data):
    global is_user_logged_in, username_of_user_logged_in

    if is_user_logged_in == True and username_of_user_logged_in != "":
        View_HomeUI._popup_generic_message("You must be logged out to delete \nan account")
        return

    #So user knows program is busy
    View_HomeUI._popup_busy_deleting_user(sender, app_data, user_data)

    result =  Model._delete_user_data_files(sender, app_data, user_data)

    View_HomeUI._popup_delete_user_result(dpg.get_value(user_data[1]), result)

    #delete corresponding dpg items in memory
    for gear in list(gears):
        gearButtonToRemove = gears.pop(str(gear))
        dpg.delete_item(gearButtonToRemove["gear_button_tag"])

    # So busy popup goes away
    _check_window_exists(View_HomeUI.BUSY_DELETING_USER_WINDOW_TAG)

    #So homescreen header text changes back to default
    dpg.set_value("homescreen_header_text", View_HomeUI.homescreen_header_default_text)

# -----------------------------------------------------------------------------------------
def _load_user_data(sender, app_data, user_data):
    global is_user_logged_in, username_of_user_logged_in

    if is_user_logged_in == True and username_of_user_logged_in != "":
        View_HomeUI._popup_generic_message("You must be logged out to login to \nan account")
        return

    result = Model._verify_user_password(sender, app_data, user_data)
    username = result[0]
    login_result = result[1]

    if result == "User not in database":
        View_HomeUI._popup_generic_message(f"User not in database")
        return

    elif login_result == False:
        View_HomeUI._popup_generic_message(f'Password for User: "{username}" is invalid.')

    elif login_result == True:
        View_HomeUI._clear_gear_buttons()
        is_user_logged_in = True
        username_of_user_logged_in = username
        dpg.set_value("homescreen_header_text", f"Gear for {username}")
        list_of_gears = Model.load_deployment_gear(username)
        if list_of_gears is not None:
            View_HomeUI._load_gear_buttons(username, list_of_gears)
        View_HomeUI._popup_generic_message(f'Successfully logged in as User: "{username}"')