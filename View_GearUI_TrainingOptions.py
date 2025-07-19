import dearpygui.dearpygui as dpg

gear_windows = {}  # Tracks all gear-specific UI metadata

def add_entry_callback(sender, app_data, user_data):
    gear = user_data
    meta = gear_windows[gear]

    i = meta['entry_counter']
    table_tag = meta['table_tag']

    with dpg.table_row(parent=table_tag):
        inputTextTag = f"{gear}_entry_{i}_inputText"
        inputFloatTag = f"{gear}_entry_{i}_inputFloat"
        inputIntTag = f"{gear}_entry_{i}_inputInt"

        dpg.add_input_text(label="", width=-1, default_value=f"Item {i+1}", tag=inputTextTag)
        dpg.add_input_float(label="", width=-1, default_value=0.0, format="%.2f", tag=inputFloatTag)
        dpg.add_input_int(label="", width=-1, default_value=1, tag=inputIntTag)

        meta['entries'][f"Entry_{i}"] = {
            "inputText_Tag": inputTextTag,
            "inputFloat_Tag": inputFloatTag,
            "inputInt_Tag": inputIntTag
        }

    meta['entry_counter'] += 1


def start(sender, app_data, user_data):
    gear = user_data
    window_tag = f"{gear}_window"
    child_tag = f"{gear}_child"
    table_tag = f"{gear}_table"
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    if gear in gear_windows:
        dpg.configure_item(window_tag, show=True)
        return

    # Initialize data for new gear
    gear_windows[gear] = {
        'window_tag': window_tag,
        'child_tag': child_tag,
        'table_tag': table_tag,
        'entry_counter': 0,
        'entries': {}
    }

    with dpg.window(label=f" Training Options For {gear}", tag=window_tag, width=410, height=500,
                    on_close=lambda: dpg.configure_item(window_tag, show=False), modal=True):
        dpg.add_text("What would you like to do?")

        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Performance Tracking", width=button_width, height=100)
        with dpg.group(horizontal=True):
                dpg.add_spacer(width=padding)
                dpg.add_button(label="Train", width=button_width, height=100)

        #dpg.add_button(label="Add Entry", callback=add_entry_callback, user_data=gear)
