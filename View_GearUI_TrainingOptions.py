import dearpygui.dearpygui as dpg
import View_GearUI_TrainingOptions_Train
import View_GearUI_TrainingOptions_Track


def start(sender, app_data, user_data):
    gear = user_data
    window_tag = f"{gear}_window"
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    if dpg.does_item_exist(window_tag):
        dpg.delete_item(window_tag)


    with dpg.window(label=f" Training Options For {gear}", tag=window_tag, width=430, height=558,
                    on_close=lambda: dpg.delete_item(window_tag)):
        dpg.add_text("What would you like to do?")

        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Performance Tracking", callback=View_GearUI_TrainingOptions_Track.show_training_graph, width=button_width, height=100, user_data=gear)
        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Train", callback=View_GearUI_TrainingOptions_Train.show_timer, width=button_width, height=100, user_data=gear)

