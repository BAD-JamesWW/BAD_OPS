# © 2025 B.A.D. Black Apex Development LLC
# All rights reserved.
# This software and its associated name, logo, and branding are the intellectual property of
# B.A.D. Black Apex Development LLC — registered in the State of Ohio (Entity #5448030).
# Unauthorized use, reproduction, or distribution is prohibited and may violate
# copyright, trademark, and unfair competition laws.


#Description: Responsible for controlling the flow of the program.
import View_HomeUI
import View_GearUI_TrainingOptions
import Model
import dearpygui.dearpygui as dpg
import pygame
import os

pygame.mixer.init()

gears = dict()

#-----------------------------------------------------------------------------------------
def main():
    View_HomeUI._create_homeUI()

if __name__ == "__main__":
    main()

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

def _show_window(previous_window_tag):
    dpg.show_item(previous_window_tag)

def _hide_window(previous_window_tag):
    dpg.hide_item(previous_window_tag)

def _delete_window(window_tag):
    dpg.delete_item(window_tag)

def _check_window_exists(window_tag):
    if dpg.does_item_exist(window_tag):
        dpg.delete_item(window_tag)

def _add_gear(sender, app_data, user_data):
    button_container = user_data[0]
    input_tag = user_data[1]
    home_ui_window = user_data[2]
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    View_HomeUI.inputInProgress = False

    # === Gear Button Theme (Red Highlight) ===
    with dpg.theme() as red_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active


    if dpg.is_item_shown(input_tag):
        gear_name = str(dpg.get_value(input_tag).strip())

        if gear_name and gears.get(gear_name, "doesNotExist") == "doesNotExist":
            gears[gear_name] = {"gear_button_tag": gear_name}
            with dpg.group(horizontal=True, parent=button_container):
                dpg.add_spacer(width=padding)
                dpg.add_button(label=f"{gear_name}", width=button_width, height=100, tag=gear_name,
                               callback=View_GearUI_TrainingOptions.start, user_data=[gear_name, home_ui_window])
                dpg.bind_item_theme(gear_name, red_button_theme)
                Model.save_deployment_gear(f"{gear_name}")
            dpg.hide_item(input_tag)
            dpg.set_value(input_tag, "")
        else:
            View_HomeUI._popup_add_gear_failed(isInputEmpty=(dpg.get_value(input_tag).strip() == ""))
            dpg.set_value(input_tag, "")
    else:
        dpg.show_item(input_tag)

def _remove_gear(sender, app_data, user_data):
    View_HomeUI.inputInProgress = False
    input_tag = user_data[1]
    if dpg.is_item_shown(input_tag):
        gear_name = dpg.get_value(input_tag).strip()
        if gear_name and gears.get(str(gear_name), "doesNotExist") != "doesNotExist":
            gearButtonToRemove = gears.pop(str(gear_name))
            dpg.delete_item(gearButtonToRemove["gear_button_tag"])
            Model.delete_deployment_gear_time(gearButtonToRemove["gear_button_tag"])
            Model.delete_deployment_gear(gearButtonToRemove["gear_button_tag"])
            dpg.hide_item(input_tag)
            dpg.set_value(input_tag, "")
        else:
            View_HomeUI._popup_remove_gear_failed(isInputEmpty=(dpg.get_value(input_tag).strip() == ""))
            dpg.set_value(input_tag, "")
    else:
        dpg.show_item(input_tag)

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