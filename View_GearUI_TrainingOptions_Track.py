import dearpygui.dearpygui as dpg
import Model
import Control

def time_to_milliseconds(time_str):
    if time_str.count(":") != 2 or "." not in time_str:
        raise ValueError(f"Invalid time format: {time_str}")
    hours, minutes, rest = time_str.split(':')
    seconds, milliseconds = rest.split('.')
    return (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds)

def format_milliseconds(ms):
    total_seconds = ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = int(total_seconds % 60)
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Store annotation tags globally for toggle use
annotation_tags = []
annotations_visible = True  # Toggle state tracker

def toggle_annotations():
    global annotations_visible
    annotations_visible = not annotations_visible
    for tag in annotation_tags:
        dpg.configure_item(tag, show=annotations_visible)

def show_training_graph(sender=None, app_data=None, user_data=None):
    global annotation_tags
    annotation_tags.clear()  # Reset when graph is refreshed

    gear = user_data
    training_data = Model.get_sorted_times_by_key(gear)

    if len(training_data) == 0:
        return

    Control.play_sound("assets/audio/ui_sound_02.wav", wait=False)

    line_segments = []
    current_x, current_y = [], []
    scatter_x, scatter_y = [], []
    botched_x, botched_y = [], []
    annotations = []

    session_index = 1
    prev_y = None

    total_time = 0
    count = 0

    for entry in training_data:
        ms = entry["milliseconds"]
        if ms == "EightySix":
            if current_x and current_y:
                line_segments.append((current_x, current_y))
                current_x, current_y = [], []
            if prev_y is not None:
                botched_x.append(session_index)
                botched_y.append(prev_y)
                annotations.append((session_index, prev_y, "EightySix"))
        else:
            y_val = ms / 1000
            total_time += ms
            count += 1
            current_x.append(session_index)
            current_y.append(y_val)
            scatter_x.append(session_index)
            scatter_y.append(y_val)
            annotations.append((session_index, y_val, format_milliseconds(ms)))
            prev_y = y_val
        session_index += 1

    if current_x and current_y:
        line_segments.append((current_x, current_y))

    avg_time = total_time // count if count > 0 else 0
    avg_time_formatted = format_milliseconds(avg_time)

    graph_window_tag = "training_graph_window"
    plot_tag = "training_graph_plot"
    y_axis_tag = "training_graph_yaxis"
    x_axis_tag = "training_graph_xaxis"
    scatter_tag = "training_graph_scatter"
    botched_tag = "botched_scatter"

    Control._check_window_exists(graph_window_tag)

    with dpg.window(tag=graph_window_tag, width=445, height=570, no_move=True, no_resize=True, no_collapse=True, pos=(0, 0), on_close=lambda: Control.play_sound("assets/audio/ui_sound_05.wav", wait=False)):
        dpg.add_text(f"Training Session Scores for {gear}")

        # === Parent Window Theme ===
        with dpg.theme() as parent_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                # Title bar background (normal and active)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0, 0, 0, 250))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 0, 0, 250))
                # Optional: border color (dark grey)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (20, 20, 20, 150))
        dpg.bind_item_theme(graph_window_tag, parent_theme)

        # === Red Button Highlight Theme ===
        with dpg.theme() as red_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active

        with dpg.plot(label="Score Over Time", height=470, width=430, tag=plot_tag, no_box_select=True, no_menus=True):
            dpg.add_plot_legend()
            with dpg.plot_axis(dpg.mvXAxis, label="", no_tick_labels=True, tag=x_axis_tag):
                dpg.configure_item(x_axis_tag, no_highlight=True)
                pass
            dpg.add_plot_axis(dpg.mvYAxis, label="Time (seconds)", tag=y_axis_tag)
            dpg.configure_item(y_axis_tag, no_highlight=True)


            for idx, (lx, ly) in enumerate(line_segments):
                line_tag = f"line_segment_{idx}"
                dpg.add_line_series(lx, ly, tag=line_tag, parent=y_axis_tag)
                with dpg.theme() as line_theme:
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
                dpg.bind_item_theme(line_tag, line_theme)

            dpg.add_scatter_series(scatter_x, scatter_y, label="Time", tag=scatter_tag, parent=y_axis_tag)

            if botched_x:
                dpg.add_scatter_series(botched_x, botched_y, label="EightySix", tag=botched_tag, parent=y_axis_tag)

        # Below the plot
        with dpg.group(horizontal=True):
            dpg.add_button(label="Toggle Annotations",tag="toggle_annotations", callback=toggle_annotations)
            dpg.bind_item_theme("toggle_annotations", red_button_theme)
            dpg.add_text(f"Avg Speed: {avg_time_formatted}")

    # Themes
    with dpg.theme() as scatter_theme:
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (100, 0, 0, 255), category=dpg.mvThemeCat_Plots)

    with dpg.theme() as botched_theme:
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (255, 255, 0, 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (200, 200, 0, 255), category=dpg.mvThemeCat_Plots)

    dpg.bind_item_theme(scatter_tag, scatter_theme)
    if botched_x:
        dpg.bind_item_theme(botched_tag, botched_theme)

    # Add annotations that match exact dot values
    for i, (x, y, label) in enumerate(annotations):
        tag = f"label_{i}"
        annotation_tags.append(tag)
        dpg.add_plot_annotation(
            default_value=(x, y - 0.2),
            label=label,
            parent=plot_tag,
            clamped=True,
            tag=tag
        )