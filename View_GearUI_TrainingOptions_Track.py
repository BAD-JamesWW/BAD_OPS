import dearpygui.dearpygui as dpg
import Model

def show_training_graph():
    training_data = Model.get_past_scores()
    """
    Plots a line graph of training session scores using Dear PyGui.

    Args:
        training_data (dict): Dictionary with session IDs as keys and scores as values.
    """

    # Ensure data is sorted by session ID
    session_ids = list(training_data.keys())
    scores = [training_data[k] for k in session_ids]

    # Unique tag for this graph window
    graph_window_tag = "training_graph_window"
    plot_tag = "training_graph_plot"
    x_axis_tag = "training_graph_xaxis"
    y_axis_tag = "training_graph_yaxis"
    series_tag = "training_graph_series"

    # If it already exists, delete and recreate
    if dpg.does_item_exist(graph_window_tag):
        dpg.delete_item(graph_window_tag)

    with dpg.window(label="Training Graph", tag=graph_window_tag, width=430, height=550, pos=(100, 100), modal=True, no_resize=False):
        dpg.add_text("Training Session Scores")

        with dpg.plot(label="Score Over Time", height=500, width=430, tag=plot_tag):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Session ID", tag=x_axis_tag)
            dpg.add_plot_axis(dpg.mvYAxis, label="Score", tag=y_axis_tag)
            dpg.add_line_series(session_ids, scores, label="Score", parent=y_axis_tag, tag=series_tag)
