import dearpygui.dearpygui as dpg
import View_GearUI_TrainingOptions_Train
import View_GearUI_TrainingOptions_Track
import pygame
import os


def start(sender, app_data, user_data):
    gear = user_data[0]
    previous_window = user_data[1]
    window_tag = f"{gear}_window"
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    if dpg.does_item_exist(window_tag):
        dpg.delete_item(window_tag)

    dpg.hide_item(previous_window)
    play_sound("assets/audio/ui_sound_01.wav", wait=False)

    with dpg.window(label=f" Training Options For {gear}", tag=window_tag, width=430, height=570,
                    on_close=lambda: (dpg.show_item(previous_window), play_sound("assets/audio/ui_sound_05.wav", wait=False), dpg.delete_item(window_tag)), no_move=True):
        dpg.add_text("What would you like to do?")

        with dpg.theme() as training_options_full_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                # Transparent window background
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 50))
                # Title bar background (normal and active)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0, 0, 0, 250))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 0, 0, 250))
                # Optional: border color (dark grey)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (20, 20, 20, 150))

        dpg.bind_item_theme(window_tag, training_options_full_theme)



        
        # === Red Button Highlight Theme ===
        with dpg.theme() as red_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active

        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Performance Tracking",tag="performance_tracking_button", callback=View_GearUI_TrainingOptions_Track.show_training_graph, width=button_width, height=100, user_data=gear)
                dpg.bind_item_theme("performance_tracking_button", red_button_theme)           
        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Train",tag = "train_button", callback=View_GearUI_TrainingOptions_Train.show_timer, width=button_width, height=100, user_data=[gear,window_tag])
                dpg.bind_item_theme("train_button", red_button_theme)


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