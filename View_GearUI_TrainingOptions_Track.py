import dearpygui.dearpygui as dpg
import Model

def format_milliseconds(ms):
    """Convert milliseconds to time string (MM:SS.mmm)."""
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    milliseconds = ms % 1000
    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

def show_training_graph(sender, app_data, user_data):
    gear = user_data
    training_data = Model.get_sorted_times_by_key(gear)

    if len(training_data) == 0:
        return

    session_ids = list(range(1, len(training_data) + 1))
    scores = [entry["milliseconds"] for entry in training_data]
    formatted_scores = [format_milliseconds(ms) for ms in scores]

    graph_window_tag = "training_graph_window"
    plot_tag = "training_graph_plot"
    x_axis_tag = "training_graph_xaxis"
    y_axis_tag = "training_graph_yaxis"
    line_tag = "training_graph_line"
    scatter_tag = "training_graph_scatter"

    if dpg.does_item_exist(graph_window_tag):
        dpg.delete_item(graph_window_tag)

    with dpg.window(label="Training Graph", tag=graph_window_tag, width=430, height=550, pos=(100, 100), modal=True, no_resize=False):
        dpg.add_text(f"Training Session Scores for {gear}")

        with dpg.plot(label="Score Over Time", height=500, width=430, tag=plot_tag):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Session #", tag=x_axis_tag)
            dpg.add_plot_axis(dpg.mvYAxis, label="Milliseconds (Lower is Better)", tag=y_axis_tag)

            dpg.add_line_series(session_ids, scores, label="Score", parent=y_axis_tag, tag=line_tag)
            dpg.add_scatter_series(session_ids, scores, label="Dots", parent=y_axis_tag, tag=scatter_tag)

            # Reverse the Y-axis so lower scores appear higher
            min_score = min(scores)
            max_score = max(scores)
            dpg.set_axis_limits(y_axis_tag, max_score + 100, min_score - 100)

            # Add visible text labels below each point
            for i, (x, y, label) in enumerate(zip(session_ids, scores, formatted_scores)):
                dpg.add_plot_annotation(
                    default_value=(x, y - 50),  # Offset text 50ms below the dot
                    label=label,
                    parent=plot_tag,
                    clamped=True,
                    tag=f"label_{i}"
                )
