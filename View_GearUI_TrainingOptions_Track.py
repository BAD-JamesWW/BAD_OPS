import dearpygui.dearpygui as dpg
import Model

def format_milliseconds(ms):
    """Convert milliseconds to time string (HH:MM:SS.mmm)."""
    total_seconds = ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def show_training_graph(sender=None, app_data=None, user_data=None):
    gear = user_data
    training_data = Model.get_sorted_times_by_key(gear)

    if len(training_data) == 0:
        return

    session_ids = list(range(1, len(training_data) + 1))
    raw_scores = [entry["milliseconds"] for entry in training_data]
    scores_in_seconds = [ms / 1000 for ms in raw_scores]  # Plot in seconds
    formatted_scores = [format_milliseconds(ms) for ms in raw_scores]

    graph_window_tag = "training_graph_window"
    plot_tag = "training_graph_plot"
    y_axis_tag = "training_graph_yaxis"
    line_tag = "training_graph_line"
    scatter_tag = "training_graph_scatter"

    if dpg.does_item_exist(graph_window_tag):
        dpg.delete_item(graph_window_tag)

    with dpg.window(label="Training Graph", tag=graph_window_tag, width=480, height=580, modal=True, no_resize=False, pos=(100, 100)):
        dpg.add_text(f"Training Session Scores for {gear}")

        with dpg.plot(label="Score Over Time", height=500, width=460, tag=plot_tag):
            dpg.add_plot_legend()

            # X-axis hidden
            with dpg.plot_axis(dpg.mvXAxis, label="", no_tick_labels=True):
                pass

            # Y-axis shows time in seconds
            dpg.add_plot_axis(dpg.mvYAxis, label="Time (seconds)", tag=y_axis_tag)

            dpg.add_line_series(session_ids, scores_in_seconds, label="Easy Visual", tag=line_tag, parent=y_axis_tag)
            dpg.add_scatter_series(session_ids, scores_in_seconds, label="Time", tag=scatter_tag, parent=y_axis_tag)

    # Themes for dots and lines
    with dpg.theme() as scatter_theme:
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (100, 0, 0, 255), category=dpg.mvThemeCat_Plots)

    with dpg.theme() as line_theme:
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)

    dpg.bind_item_theme(line_tag, line_theme)
    dpg.bind_item_theme(scatter_tag, scatter_theme)

    # Add annotation labels below each data point
    for i, (x, y, label) in enumerate(zip(session_ids, scores_in_seconds, formatted_scores)):
        dpg.add_plot_annotation(
            default_value=(x, y - 0.2),
            label=label,
            parent=plot_tag,
            clamped=True,
            tag=f"label_{i}"
        )
