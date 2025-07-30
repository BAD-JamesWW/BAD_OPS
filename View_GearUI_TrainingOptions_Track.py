import dearpygui.dearpygui as dpg
import Model

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

def show_training_graph(sender=None, app_data=None, user_data=None):
    gear = user_data
    training_data = Model.get_sorted_times_by_key(gear)

    if len(training_data) == 0:
        return

    line_segments = []
    current_x, current_y = [], []
    scatter_x, scatter_y = [], []
    botched_x, botched_y = [], []
    annotations = []

    session_index = 1
    prev_y = None

    for entry in training_data:
        ms = entry["milliseconds"]
        if ms == "botched":
            if current_x and current_y:
                line_segments.append((current_x, current_y))
                current_x, current_y = [], []
            if prev_y is not None:
                botched_x.append(session_index)
                botched_y.append(prev_y)
                annotations.append((session_index, prev_y, "BOTCHED"))
        else:
            y_val = ms / 1000
            current_x.append(session_index)
            current_y.append(y_val)
            scatter_x.append(session_index)
            scatter_y.append(y_val)
            annotations.append((session_index, y_val, format_milliseconds(ms)))
            prev_y = y_val
        session_index += 1

    if current_x and current_y:
        line_segments.append((current_x, current_y))

    graph_window_tag = "training_graph_window"
    plot_tag = "training_graph_plot"
    y_axis_tag = "training_graph_yaxis"
    scatter_tag = "training_graph_scatter"
    botched_tag = "botched_scatter"

    if dpg.does_item_exist(graph_window_tag):
        dpg.delete_item(graph_window_tag)

    with dpg.window(label="Training Graph", tag=graph_window_tag, width=480, height=580, modal=True, no_resize=False, pos=(100, 100)):
        dpg.add_text(f"Training Session Scores for {gear}")
        with dpg.plot(label="Score Over Time", height=500, width=460, tag=plot_tag):
            dpg.add_plot_legend()
            with dpg.plot_axis(dpg.mvXAxis, label="", no_tick_labels=True):
                pass
            dpg.add_plot_axis(dpg.mvYAxis, label="Time (seconds)", tag=y_axis_tag)

            for idx, (lx, ly) in enumerate(line_segments):
                line_tag = f"line_segment_{idx}"
                dpg.add_line_series(lx, ly, tag=line_tag, parent=y_axis_tag)
                with dpg.theme() as line_theme:
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
                dpg.bind_item_theme(line_tag, line_theme)

            dpg.add_scatter_series(scatter_x, scatter_y, label="Time", tag=scatter_tag, parent=y_axis_tag)

            if botched_x:
                dpg.add_scatter_series(botched_x, botched_y, label="Botched", tag=botched_tag, parent=y_axis_tag)

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
        dpg.add_plot_annotation(
            default_value=(x, y - 0.2),
            label=label,
            parent=plot_tag,
            clamped=True,
            tag=f"label_{i}"
        )