from dearpygui import dearpygui as dpg
import View_GearUI_TrainingOptions
import Model
import pygame
import os

NON_EXISTENT_GEAR_WINDOW_TAG = "non_existent_category_window"
NON_EXISTENT_GEAR_HANDLER_TAG = "non_existent_category_handler"
ALREADY_EXISTENT_GEAR_WINDOW_TAG = "already_existent_category_window"
ALREADY_EXISTENT_GEAR_HANDLER_TAG = "already_existent_category_handler"
gears = dict()

dpg.create_context()

# === Gear Button Theme (Red Highlight) ===
with dpg.theme() as red_button_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active

def _add_gear(sender, app_data, user_data):
    button_container = user_data[0]
    input_field = user_data[1]
    home_ui_window = user_data[2]
    loading_status = user_data[3]
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    #So sound plays ony if loading status is false
    if loading_status == False:
        play_sound("assets/audio/ui_sound_03.wav", wait=False)

    if dpg.is_item_shown(input_field):
        gear_name = str(dpg.get_value(input_field).strip())

        if gear_name and gears.get(gear_name, "doesNotExist") == "doesNotExist":
            gears[gear_name] = {"gear_button_tag": gear_name}
            with dpg.group(horizontal=True, parent=button_container):
                dpg.add_spacer(width=padding)
                dpg.add_button(label=f"{gear_name}", width=button_width, height=100, tag=gear_name,
                               callback=View_GearUI_TrainingOptions.start, user_data=[gear_name, home_ui_window])
                dpg.bind_item_theme(gear_name, red_button_theme)
                Model.save_deployment_gear(f"{gear_name}")
            dpg.hide_item(input_field)
            dpg.set_value(input_field, "")
        else:
            _popup_add_gear_failed(isInputEmpty=(dpg.get_value(input_field).strip() == ""))
            dpg.set_value(input_field, "")
    else:
        dpg.show_item(input_field)

def _remove_gear(sender, app_data, user_data):
    play_sound("assets/audio/ui_sound_03.wav", wait=False)
    input_field = user_data[1]
    if dpg.is_item_shown(input_field):
        gear_name = dpg.get_value(input_field).strip()
        if gear_name and gears.get(str(gear_name), "doesNotExist") != "doesNotExist":
            gearButtonToRemove = gears.pop(str(gear_name))
            dpg.delete_item(gearButtonToRemove["gear_button_tag"])
            Model.delete_deployment_gear_time(gearButtonToRemove["gear_button_tag"])
            Model.delete_deployment_gear(gearButtonToRemove["gear_button_tag"])
            dpg.hide_item(input_field)
            dpg.set_value(input_field, "")
        else:
            _popup_remove_gear_failed(isInputEmpty=(dpg.get_value(input_field).strip() == ""))
            dpg.set_value(input_field, "")
    else:
        dpg.show_item(input_field)

def _nuke_gear(sender, app_data, user_data):
    if dpg.does_item_exist("nuke_confirm_window"):
        dpg.delete_item("nuke_confirm_window")

    play_sound("assets/audio/ui_sound_03.wav", wait=False)

    def _confirm():
        dpg.delete_item("nuke_confirm_window")
        for gear in list(gears):
            gearButtonToRemove = gears.pop(str(gear))
            dpg.delete_item(gearButtonToRemove["gear_button_tag"])
            Model.delete_deployment_gear(gearButtonToRemove["gear_button_tag"])
            Model.delete_deployment_gear_time(gearButtonToRemove["gear_button_tag"])

    def _cancel():
        dpg.delete_item("nuke_confirm_window")

    with dpg.window(label="Confirm Nuke", modal=True, tag="nuke_confirm_window", no_title_bar=True, width=360, height=150, pos=(300, 300)):
        dpg.add_text("Are you sure you want to nuke all gear?\nThis action cannot be undone.", wrap=330)
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Yes", width=75, callback=_confirm)
            dpg.add_button(label="No", width=75, callback=_cancel)

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