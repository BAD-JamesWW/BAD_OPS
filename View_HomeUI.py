# © 2025 B.A.D. Black Apex Development LLC
# All rights reserved.
# This software and its associated name, logo, and branding are the intellectual property of
# B.A.D. Black Apex Development LLC — registered in the State of Ohio (Entity #5448030).
# Unauthorized use, reproduction, or distribution is prohibited and may violate
# copyright, trademark, and unfair competition laws.


# Description: Responsible for the Home UI as a whole.
from dearpygui import dearpygui as dpg
import Model
import Control


dpg.create_context()

inputInProgress = False
homescreen_header_default_text = "Gear"
NON_EXISTENT_GEAR_WINDOW_TAG = "non_existent_category_window"
NON_EXISTENT_GEAR_HANDLER_TAG = "non_existent_category_handler"
ALREADY_EXISTENT_GEAR_WINDOW_TAG = "already_existent_category_window"
ALREADY_EXISTENT_GEAR_HANDLER_TAG = "already_existent_category_handler"
ALREADY_EXISTENT_USER_WINDOW_TAG = "already_existent_user_window"
ALREADY_EXISTENT_USER_HANDLER_TAG = "already_existent_user_handler"
USER_DELETION_RESULT_WINDOW_TAG = "user_deletion_result_window"
USER_DELETION_RESULT_HANDLER_TAG = "user_deletion_result_handler"
USER_NOT_IN_DATABASE_WINDOW_TAG = "user_not_in_databse_window"
USER_NOT_IN_DATABASE_HANDLER_TAG = "user_not_in_database_handler"
USER_CREATION_RESULT_WINDOW_TAG = "user_creation_result_window"
USER_CREATION_RESULT_HANDLER_TAG = "user_creation_result_handler"
USER_LOAD_RESULT_WINDOW_TAG = "user_load_result_window"
USER_LOAD_RESULT_HANDLER_TAG = "user_load_result_handler"
BUSY_CREATING_USER_WINDOW_TAG = "busy_creating_user_window"
BUSY_DELETING_USER_WINDOW_TAG = "busy_deleting_user_window"



def _popup_remove_gear_failed(isInputEmpty):
    if dpg.does_item_exist(NON_EXISTENT_GEAR_WINDOW_TAG):
        dpg.delete_item(NON_EXISTENT_GEAR_WINDOW_TAG)
    if dpg.does_item_exist(NON_EXISTENT_GEAR_HANDLER_TAG):
        dpg.delete_item(NON_EXISTENT_GEAR_HANDLER_TAG)

    msg = "Please enter valid input" if isInputEmpty else "Gear Doesn't exist"
    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=NON_EXISTENT_GEAR_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(NON_EXISTENT_GEAR_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=NON_EXISTENT_GEAR_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(NON_EXISTENT_GEAR_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(NON_EXISTENT_GEAR_WINDOW_TAG, NON_EXISTENT_GEAR_HANDLER_TAG)
    except Exception:
        pass

def _popup_add_gear_failed(isInputEmpty):
    if dpg.does_item_exist(ALREADY_EXISTENT_GEAR_WINDOW_TAG):
        dpg.delete_item(ALREADY_EXISTENT_GEAR_WINDOW_TAG)
    if dpg.does_item_exist(ALREADY_EXISTENT_GEAR_HANDLER_TAG):
        dpg.delete_item(ALREADY_EXISTENT_GEAR_HANDLER_TAG)

    msg = "Enter a valid gear name" if isInputEmpty else "Gear Already Exists"
    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=ALREADY_EXISTENT_GEAR_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(ALREADY_EXISTENT_GEAR_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=ALREADY_EXISTENT_GEAR_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(ALREADY_EXISTENT_GEAR_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(ALREADY_EXISTENT_GEAR_WINDOW_TAG, ALREADY_EXISTENT_GEAR_HANDLER_TAG)
    except Exception:
        pass

def _popup_create_user_failed(sender, app_data, user_data):
    if dpg.does_item_exist(ALREADY_EXISTENT_USER_WINDOW_TAG):
        dpg.delete_item(ALREADY_EXISTENT_USER_WINDOW_TAG)
    if dpg.does_item_exist(ALREADY_EXISTENT_USER_HANDLER_TAG):
        dpg.delete_item(ALREADY_EXISTENT_USER_HANDLER_TAG)

    msg = f"User: {dpg.get_value(user_data[1])} already exists"
    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=ALREADY_EXISTENT_USER_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(ALREADY_EXISTENT_USER_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=ALREADY_EXISTENT_USER_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(ALREADY_EXISTENT_USER_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(ALREADY_EXISTENT_USER_WINDOW_TAG, ALREADY_EXISTENT_USER_HANDLER_TAG)
    except Exception:
        pass

def _popup_user_not_in_database(sender, app_data, user_data):
    if dpg.does_item_exist(USER_NOT_IN_DATABASE_WINDOW_TAG):
        dpg.delete_item(USER_NOT_IN_DATABASE_WINDOW_TAG)
    if dpg.does_item_exist(USER_NOT_IN_DATABASE_HANDLER_TAG):
        dpg.delete_item(USER_NOT_IN_DATABASE_HANDLER_TAG)

    msg = f"User: {dpg.get_value(user_data[1])} not in database"
    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=USER_NOT_IN_DATABASE_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(USER_NOT_IN_DATABASE_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=USER_NOT_IN_DATABASE_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(USER_NOT_IN_DATABASE_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(USER_NOT_IN_DATABASE_WINDOW_TAG, USER_NOT_IN_DATABASE_HANDLER_TAG)
    except Exception:
        pass

def _popup_user_load_result(sender, app_data, user_data):
    if dpg.does_item_exist(USER_LOAD_RESULT_WINDOW_TAG):
        dpg.delete_item(USER_LOAD_RESULT_WINDOW_TAG)
    if dpg.does_item_exist(USER_LOAD_RESULT_HANDLER_TAG):
        dpg.delete_item(USER_LOAD_RESULT_HANDLER_TAG)

    if user_data[1] == False:
        msg = f'Password for User: "{user_data[0]}" is invalid.'
    else:
        msg = f'Successfully logged in as User: "{user_data[0]}"'

    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=USER_LOAD_RESULT_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(USER_LOAD_RESULT_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=USER_LOAD_RESULT_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(USER_LOAD_RESULT_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(USER_LOAD_RESULT_WINDOW_TAG, USER_LOAD_RESULT_HANDLER_TAG)
    except Exception:
        pass

def _popup_busy_creating_user(sender, app_data, user_data):
    if dpg.does_item_exist(BUSY_CREATING_USER_WINDOW_TAG):
        dpg.delete_item(BUSY_CREATING_USER_WINDOW_TAG)

    msg = f" Creating data for User: {dpg.get_value(user_data[1])}..."
    with dpg.window(label="Info", modal=True, no_collapse=True, no_close=True,
                    tag=BUSY_CREATING_USER_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(BUSY_CREATING_USER_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

def _popup_busy_deleting_user(sender, app_data, user_data):
    if dpg.does_item_exist(BUSY_DELETING_USER_WINDOW_TAG):
        dpg.delete_item(BUSY_DELETING_USER_WINDOW_TAG)

    msg = f"Deleting data for User: {dpg.get_value(user_data[1])}..."
    with dpg.window(label="Info", modal=True, no_collapse=True, no_close=True,
                    tag=BUSY_DELETING_USER_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(BUSY_DELETING_USER_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

def _popup_delete_user_result(username: str, result: str):
    if dpg.does_item_exist(USER_DELETION_RESULT_WINDOW_TAG):
        dpg.delete_item(USER_DELETION_RESULT_WINDOW_TAG)
    if dpg.does_item_exist(USER_DELETION_RESULT_HANDLER_TAG):
        dpg.delete_item(USER_DELETION_RESULT_HANDLER_TAG)

    if result == "Does not exist":
        msg = f"User: {username} doesn't exist"
    else:
        msg = f"User: {username} successfully derezzed"

    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=USER_DELETION_RESULT_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(USER_DELETION_RESULT_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=USER_DELETION_RESULT_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(USER_DELETION_RESULT_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(USER_DELETION_RESULT_WINDOW_TAG, USER_DELETION_RESULT_HANDLER_TAG)
    except Exception:
        pass



def _popup_user_creation_result(username: str):
    if dpg.does_item_exist(USER_CREATION_RESULT_WINDOW_TAG):
        dpg.delete_item(USER_CREATION_RESULT_WINDOW_TAG)
    if dpg.does_item_exist(USER_CREATION_RESULT_HANDLER_TAG):
        dpg.delete_item(USER_CREATION_RESULT_HANDLER_TAG)

    msg = f"Identity diskspace allocated - \nUser: {username} brought online."

    with dpg.window(label="Info", modal=True, no_collapse=True,
                    tag=USER_CREATION_RESULT_WINDOW_TAG, width=300, height=100):
        dpg.add_text(msg)
        vw, vh = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_pos(USER_CREATION_RESULT_WINDOW_TAG, [vw // 2 - 150, vh // 2 - 50])

    with dpg.item_handler_registry(tag=USER_CREATION_RESULT_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(USER_CREATION_RESULT_WINDOW_TAG))
    try:
        dpg.bind_item_handler_registry(USER_CREATION_RESULT_WINDOW_TAG, USER_CREATION_RESULT_HANDLER_TAG)
    except Exception:
        pass

#Clears gear buttons displayed on the home screen
def _clear_gear_buttons():
    if dpg.does_item_exist("button_container_home_ui"):
        for child in (dpg.get_item_children("button_container_home_ui", 1) or []):
            dpg.delete_item(child)

def _show_input_field(sender, app_data, user_data):
    global inputInProgress

    if inputInProgress == True:
        return
    inputInProgress = True
    
    button_container = user_data[0]
    fieldType = user_data[1]

    #To allow extra situational data to be passed through a call
    try:
        extra_data_slot_01 = user_data[2]
    except IndexError:
        extra_data_slot_01 = None

    input_tag = f"gear_input_field_{fieldType}"

    # Remove old input field if it exists
    Control._check_window_exists(input_tag)

    # Get all children of the parent
    children = dpg.get_item_children(button_container, 1)  # slot 1 = item slot for child items

    # Choose an item to insert before, or None if no children exist
    before_tag = children[0] if children else None

    # Create the input field with proper callback and data
    if fieldType == "add":
        Control.play_sound("assets/audio/ui_sound_03.wav", wait=False)
        dpg.add_input_text(
            parent=button_container,
            label="Enter gear name:",
            tag=input_tag,
            before=before_tag,
            on_enter=True,
            callback=lambda s, a, u: Control._add_gear(dpg.get_value(input_tag).strip(), input_tag)
        )


    elif fieldType == "remove":
        Control.play_sound("assets/audio/ui_sound_03.wav", wait=False)
        dpg.add_input_text(
            parent=button_container,
            label="Enter gear name:",
            tag=input_tag,
            before=before_tag,
            on_enter=True,
            callback=Control._remove_gear,
            user_data=[button_container, input_tag]
        )

    elif fieldType == "user_create":
        username_tag = "create_username"

        # Username input
        dpg.add_input_text(
            parent=button_container,
            hint="Enter username:",
            tag=username_tag,
            before=before_tag,
            on_enter=True,
            callback=lambda s, a, u: (
            globals().__setitem__("inputInProgress", False),
            dpg.hide_item(username_tag), #So user can't break program flow by changing the entered username
            _show_input_field(s, a, [button_container, "password_create", username_tag]),
            )
        )

    elif fieldType == "user_delete":
        username_to_delete_tag = "username_to_delete"

        # Username input
        dpg.add_input_text(
            parent=button_container,
            hint="Enter username to delete:",
            tag=username_to_delete_tag,
            before=before_tag,
            on_enter=True,
            callback=lambda s, a, u: (
            globals().__setitem__("inputInProgress", False),
            Control._delete_user_data(sender, app_data, [button_container, username_to_delete_tag]),

            #So input field is properly deleted after use
            Control._check_window_exists(username_to_delete_tag)
            )
        )

    elif fieldType == "user_to_load":
        username_to_load_tag = "username_to_load_tag"

        # Username input
        dpg.add_input_text(
            parent=button_container,
            hint="Enter name of user to load:",
            tag=username_to_load_tag,
            before=before_tag,
            on_enter=True,
            callback=lambda s, a, u: (
            globals().__setitem__("inputInProgress", False),
            dpg.hide_item(username_to_load_tag), #So user can't break program flow by changing the entered username
            _show_input_field(s, a, [button_container, "user_to_load_password", username_to_load_tag]),
            )
        )

    elif fieldType == "user_to_load_password":
        if extra_data_slot_01 is None:
            return

        user_to_load_password_tag = "user_to_load_password"
        user_to_load_username = extra_data_slot_01

        # Password input
        dpg.add_input_text(
            parent=button_container,
            hint=f"Enter password for {dpg.get_value(extra_data_slot_01)}:",
            tag=user_to_load_password_tag,
            before=before_tag,
            password=True,  # Mask input
            on_enter=True,  # Hitting Enter here triggers callback
            callback=lambda s, a, u: (
                globals().__setitem__("inputInProgress", False),
                Control._load_user_data(s, a, [button_container, user_to_load_username, user_to_load_password_tag, "home_ui_parent_window"]),

                # So input fields for username & password are properly deleted
                Control._check_window_exists(user_to_load_username),
                Control._check_window_exists(user_to_load_password_tag)
            )
        )

    elif fieldType == "password_create":
        if extra_data_slot_01 is None:
            return

        password_tag = "create_password"
        username_tag = extra_data_slot_01

        # Password input
        dpg.add_input_text(
            parent=button_container,
            hint="Enter password (Spaces Are Ignored):",
            tag=password_tag,
            before=before_tag,
            password=True,  # Mask input
            on_enter=True,  # Hitting Enter here triggers callback
            callback=lambda s, a, u: (
                globals().__setitem__("inputInProgress", False),
                Control._create_user_data(s, a, [button_container, username_tag, password_tag, "home_ui_parent_window"]),

                # So input fields for username & password are properly deleted
                Control._check_window_exists(username_tag),
                Control._check_window_exists(password_tag)
            )
        )


    elif fieldType == "account_load":
        pass
    #todo have control save username so i can then do password and only then should a load attempt be made on usualFileName with username appended that filename
    #todo if there is a user in the database that has that password attached to them
    #todo if the file doesnt exist popup will activate and this user doesn't exist
    #todo Order of operations for account functionallity is, Create-Save-Load
    #todo will need to be able to create a new user with current gear data and time data in case user doesnt make acc first
    #todo make sure no 2 username can be the same

def _load_gear(username: str, list_of_gears: list):
    if list_of_gears is not None:
        for gearName in list_of_gears:
            gear_input_tag = dpg.generate_uuid()

            Control._add_gear(gearName, gear_input_tag)

# -----------------------------------------------------------------------------------------
def _create_homeUI():
    # === Background Image ===
    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image("assets/images/bg.png")
        dpg.add_static_texture(width, height, data, tag="background_texture")

    with dpg.window(tag="background_window", no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True,
                    no_collapse=True, no_close=True, pos=(-8, -8), width=453, height=600):
        dpg.add_image("background_texture", tag="background_image")

    with dpg.window(label="Your Gear", tag="home_ui_parent_window", width=450, height=600, no_move=True, no_resize=True):
        
        dpg.configure_item("home_ui_parent_window", no_title_bar=True)

        # === Parent Window Theme (Transparent Blue) ===
        with dpg.theme() as parent_theme:
            with dpg.theme_component(0):  # mvAll
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 50))  # Transparent blue
        dpg.bind_item_theme("home_ui_parent_window", parent_theme)

        # === Red Button Highlight Theme ===
        with dpg.theme() as red_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active

        with dpg.group(horizontal=True):

            # === Middle Pane Theme (Transparent) ===
            with dpg.theme() as middle_theme:
                with dpg.theme_component(0):  # mvAll
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))

            # === Right Pane Theme (Transparent) ===
            with dpg.theme() as right_theme:
                with dpg.theme_component(0):  # mvAll
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))

            # === Middle Pane ===
            with dpg.child_window(width=370, height=400, border=False, tag="tag_middle_pane"):
                dpg.bind_item_theme("tag_middle_pane", middle_theme)

                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=150)
                    dpg.add_text(homescreen_header_default_text, tag="homescreen_header_text")


                button_container = dpg.add_child_window(width=-1, height=-1, border=False, tag="button_container_home_ui")

            # === Right Pane ===
            with dpg.child_window(width=150, height=400, border=False, tag="tag_right_pane"):
                dpg.bind_item_theme("tag_right_pane", right_theme)

                dpg.add_spacer(height=280)

                with dpg.group(horizontal=False):
                    load_account_btn = dpg.add_button(label="L User", callback=_show_input_field,
                                                        user_data=[button_container, "user_to_load"])
                    dpg.bind_item_theme(load_account_btn, red_button_theme)

                    delete_account_btn = dpg.add_button(label="- User", callback=_show_input_field,
                                                        user_data=[button_container, "user_delete"])
                    dpg.bind_item_theme(delete_account_btn, red_button_theme)

                    create_account_btn = dpg.add_button(label="+ User", callback=_show_input_field,
                                              user_data=[button_container, "user_create"])
                    dpg.bind_item_theme(create_account_btn, red_button_theme)

                    plus_btn = dpg.add_button(label="Add", callback=_show_input_field,
                                              user_data=[button_container,"add"])
                    dpg.bind_item_theme(plus_btn, red_button_theme)

                    minus_btn = dpg.add_button(label="Remove", callback=_show_input_field,
                                               user_data=[button_container,"remove"])
                    dpg.bind_item_theme(minus_btn, red_button_theme)

                    exclaim_btn = dpg.add_button(label="Nuke", callback=Control._nuke_gear)
                    dpg.bind_item_theme(exclaim_btn, red_button_theme)

# -----------------------------------------------------------------------------------------
def _run_home_ui():
    dpg.create_viewport(title="(O.P.S.) Operational Preparedness System", width=461, height=600, resizable=False)
    _create_homeUI()
    dpg.set_viewport_small_icon("assets/images/CompanyLogo.ico")
    dpg.set_viewport_large_icon("assets/images/CompanyLogo.ico")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
