import dearpygui.dearpygui as dpg
import View_GearUI_TrainingOptions_Train


def open_training_modal(sender, app_data, user_data):
    gear = user_data
    window_tag = f"{gear}_window"

    # Step 1: Hide the first modal
    dpg.configure_item(window_tag, show=False)

    # Step 2: Use a one-frame delay before opening the second modal
    def delayed_open():
        View_GearUI_TrainingOptions_Train.show_hello_modal()

    dpg.set_frame_callback(dpg.get_frame_count() + 1, delayed_open)


def start(sender, app_data, user_data):
    gear = user_data
    window_tag = f"{gear}_window"
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2


    with dpg.window(label=f" Training Options For {gear}", tag=window_tag, width=410, height=500,
                    on_close=lambda: dpg.configure_item(window_tag, show=False), modal=True):
        dpg.add_text("What would you like to do?")

        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Performance Tracking", width=button_width, height=100)
        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Train", callback=open_training_modal, width=button_width, height=100, user_data=gear)

