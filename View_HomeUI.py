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
NON_EXISTENT_GEAR_WINDOW_TAG = "non_existent_category_window"
NON_EXISTENT_GEAR_HANDLER_TAG = "non_existent_category_handler"
ALREADY_EXISTENT_GEAR_WINDOW_TAG = "already_existent_category_window"
ALREADY_EXISTENT_GEAR_HANDLER_TAG = "already_existent_category_handler"


def _popup_remove_gear_failed(isInputEmpty):
    if dpg.does_item_exist(NON_EXISTENT_GEAR_WINDOW_TAG):
        dpg.delete_item(NON_EXISTENT_GEAR_WINDOW_TAG)
    if dpg.does_item_exist(NON_EXISTENT_GEAR_HANDLER_TAG):
        dpg.delete_item(NON_EXISTENT_GEAR_HANDLER_TAG)

    msg = "Please enter valid input" if isInputEmpty else "Gear Doesn't exist"
    with dpg.window(label=msg, modal=True, no_collapse=True,
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
    with dpg.window(label=msg, modal=True, no_collapse=True,
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


def _show_input_field(sender, app_data, user_data):
    global inputInProgress

    if inputInProgress == True:
        return
    inputInProgress = True
    
    button_container = user_data[0]
    fieldType = user_data[1]
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
            callback=Control._add_gear,
            user_data=[button_container, input_tag, "home_ui_parent_window"]
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
                    dpg.add_text("Gear")


                button_container = dpg.add_child_window(width=-1, height=-1, border=False)

            # === Right Pane ===
            with dpg.child_window(width=150, height=400, border=False, tag="tag_right_pane"):
                dpg.bind_item_theme("tag_right_pane", right_theme)

                dpg.add_spacer(height=280)

                with dpg.group(horizontal=False):
                    plus_btn = dpg.add_button(label="Add", callback=_show_input_field,
                                              user_data=[button_container,"add"])
                    dpg.bind_item_theme(plus_btn, red_button_theme)

                    minus_btn = dpg.add_button(label="Remove", callback=_show_input_field,
                                               user_data=[button_container,"remove"])
                    dpg.bind_item_theme(minus_btn, red_button_theme)

                    exclaim_btn = dpg.add_button(label="Nuke", callback=Control._nuke_gear)
                    dpg.bind_item_theme(exclaim_btn, red_button_theme)

                savedGear = Model.load_deployment_gear()
                if savedGear:
                    for gearName in savedGear:
                        gear_input_tag = dpg.generate_uuid()
                        dpg.add_input_text(default_value=gearName, tag=gear_input_tag)
                        Control._add_gear(None, None, [button_container, gear_input_tag, "home_ui_parent_window", True])

# -----------------------------------------------------------------------------------------
dpg.create_viewport(title="(O.P.S.) Operational Preparedness System", width=461, height=600, resizable=False)
_create_homeUI()
dpg.set_viewport_small_icon("assets/images/CompanyLogo.ico")
dpg.set_viewport_large_icon("assets/images/CompanyLogo.ico")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
