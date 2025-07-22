#Description: Responsible for the Home UI as a whole.
from dearpygui import dearpygui as dpg
import View_HomeUI_Gear


dpg.create_context()


#-----------------------------------------------------------------------------------------
def _create_homeUI():
    with dpg.window(label="Your Gear", width=430, height=600):
        with dpg.group(horizontal=True):

            # === Left Pane ===
            #with dpg.child_window(width=380, height=400, border=True):
            #    dpg.add_text("Left Pane")
            #    for i in range(50):
            #        dpg.add_text(f"Left Item {i + 1}")

            # === Middle Pane ===
            with dpg.child_window(width=390, height=400, border=False, tag="tag_middle_pane"):
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=150)
                    dpg.add_text("Gear")

                input_field = dpg.add_input_text(parent="tag_middle_pane",label="Enter gear name:")
                dpg.hide_item(input_field)

                button_container = dpg.add_child_window(width=-1, height=-1, border=False)

            # === Right Pane ===
            with dpg.child_window(width=150, height=400, border=False):
                dpg.add_spacer(height=280)

                with dpg.group(horizontal=False):
                    dpg.add_button(label="+", callback=View_HomeUI_Gear._add_gear, user_data=[button_container, input_field])
                    dpg.add_button(label="-", callback=View_HomeUI_Gear._remove_gear, user_data=[button_container,input_field])
                    dpg.add_button(label="!", callback=View_HomeUI_Gear._nuke_gear)

    dpg.create_viewport(title="Deployment Companion", width=450, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
