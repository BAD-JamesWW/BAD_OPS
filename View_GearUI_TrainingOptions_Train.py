import dearpygui.dearpygui as dpg
import time
import Model

# Global state
timer_running = False
start_time = 0
elapsed_time = 0
timer_display_tag = "timer_display"
gear = ""

def update_timer():
    global elapsed_time
    if timer_running:
        current_time = time.perf_counter()
        elapsed_time = current_time - start_time

        hours, rem = divmod(elapsed_time, 3600)
        minutes, rem = divmod(rem, 60)
        seconds = int(rem)
        milliseconds = int((rem - seconds) * 1000)

        dpg.set_value(timer_display_tag, f"{int(hours):02}:{int(minutes):02}:{seconds:02}.{milliseconds:03}")
        dpg.set_frame_callback(dpg.get_frame_count() + 1, update_timer)

def start_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        start_time = time.perf_counter() - elapsed_time
        timer_running = True
        update_timer()

def stop_timer(sender, app_data, user_data):
    gear = user_data
    global timer_running
    timer_running = False
    Model.save_deployment_gear_time(dpg.get_value(timer_display_tag), f"{gear}")

def reset_timer():
    global timer_running, start_time, elapsed_time
    timer_running = False
    elapsed_time = 0
    dpg.set_value(timer_display_tag, "00:00:00.000")

def show_timer(sender, app_data, user_data):
    gear = user_data

    if dpg.does_item_exist("tag_timer"):
        dpg.delete_item("tag_timer")

    if not dpg.does_item_exist("tag_timer"):
        with dpg.window(label="Timer", modal=True, tag="tag_timer", width=410, height=500,
                        on_close=lambda: dpg.delete_item("tag_timer")):
            
            dpg.add_text("00:00:00.000", tag=timer_display_tag)
            dpg.add_spacer(height=10)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Start", callback=start_timer)
                dpg.add_button(label="Stop", callback=stop_timer, user_data=gear)
                dpg.add_button(label="Reset", callback=reset_timer)

            dpg.add_spacer(height=10)
            #dpg.add_button(label="Close", callback=lambda: dpg.delete_item("tag_timer"))
    else:
        dpg.configure_item("tag_timer", show=True)

    # Bring to front just in case
    dpg.focus_item("tag_timer")
