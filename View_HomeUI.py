# Description: Responsible for the Home UI as a whole.
from dearpygui import dearpygui as dpg
import View_HomeUI_Gear
import Model

dpg.create_context()

# -----------------------------------------------------------------------------------------
def _create_homeUI():
    # === Background Image ===
    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image("assets/images/bg.png")
        dpg.add_static_texture(width, height, data, tag="background_texture")

    with dpg.window(tag="background_window", no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True,
                    no_collapse=True, no_close=True, pos=(-8, -8), width=450, height=600):
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
            with dpg.child_window(width=390, height=400, border=False, tag="tag_middle_pane"):
                dpg.bind_item_theme("tag_middle_pane", middle_theme)

                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=150)
                    dpg.add_text("Gear")

                input_field = dpg.add_input_text(parent="tag_middle_pane", label="Enter gear name:")
                dpg.hide_item(input_field)

                button_container = dpg.add_child_window(width=-1, height=-1, border=False)

            # === Right Pane ===
            with dpg.child_window(width=150, height=400, border=False, tag="tag_right_pane"):
                dpg.bind_item_theme("tag_right_pane", right_theme)

                dpg.add_spacer(height=280)

                with dpg.group(horizontal=False):
                    plus_btn = dpg.add_button(label="+", callback=View_HomeUI_Gear._add_gear,
                                              user_data=[button_container, input_field, "home_ui_parent_window", False])
                    dpg.bind_item_theme(plus_btn, red_button_theme)

                    minus_btn = dpg.add_button(label="-", callback=View_HomeUI_Gear._remove_gear,
                                               user_data=[button_container, input_field])
                    dpg.bind_item_theme(minus_btn, red_button_theme)

                    exclaim_btn = dpg.add_button(label="!", callback=View_HomeUI_Gear._nuke_gear)
                    dpg.bind_item_theme(exclaim_btn, red_button_theme)

                savedGear = Model.load_deployment_gear()
                if savedGear:
                    for gearName in savedGear:
                        gear_input_tag = dpg.generate_uuid()
                        dpg.add_input_text(default_value=gearName, tag=gear_input_tag)
                        View_HomeUI_Gear._add_gear(None, None, [button_container, gear_input_tag, "home_ui_parent_window", True])

# -----------------------------------------------------------------------------------------
dpg.create_viewport(title="(O.P.S.) Operational Preparedness System", width=440, height=600, resizable=False)
_create_homeUI()
dpg.set_viewport_small_icon("assets/images/CompanyLogo.ico")
dpg.set_viewport_large_icon("assets/images/CompanyLogo.ico")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
