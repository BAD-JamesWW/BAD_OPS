# © 2025 B.A.D. Black Apex Development LLC
# All rights reserved.
# This software and its associated name, logo, and branding are the intellectual property of
# B.A.D. Black Apex Development LLC — registered in the State of Ohio (Entity #5448030).
# Unauthorized use, reproduction, or distribution is prohibited and may violate
# copyright, trademark, and unfair competition laws.

# -----------------------------------------------------------------------------------------
import dearpygui.dearpygui as dpg
import time
import threading
import random
import json
from vosk import Model as VoskModel, KaldiRecognizer
import pyaudio
import Model
import Control
import ctypes

# -----------------------------------------------------------------------------------------
# Global state
timer_running = False
start_time = 0
elapsed_time = 0
gear = ""
repetitions = 1
current_round = 0
session_active = False
manual_ready = False
manual_stop = False
manual_eighty_six = False
mic = None
stream = None
timer_display_tag = "timer_display"
rep_count_default_text = "Rep. Count:"

# -----------------------------------------------------------------------------------------
# Load voice model and audio
vosk_model = VoskModel("vosk-model-small-en-us-0.15")


# -----------------------------------------------------------------------------------------
def update_timer():
    global elapsed_time
    if timer_running:
        current_time = time.perf_counter()
        elapsed_time = current_time - start_time
        h, rem = divmod(elapsed_time, 3600)
        m, rem = divmod(rem, 60)
        s = int(rem)
        ms = int((rem - s) * 1000)
        dpg.set_value(timer_display_tag, f"{int(h):02}:{int(m):02}:{s:02}.{ms:03}")
        dpg.set_frame_callback(dpg.get_frame_count() + 1, update_timer)


# -----------------------------------------------------------------------------------------
def start_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        start_time = time.perf_counter() - elapsed_time
        timer_running = True
        update_timer()


# -----------------------------------------------------------------------------------------
def stop_timer_internal(eighty_six=False):
    global timer_running
    timer_running = False
    if not eighty_six:
        Control._save_deployment_gear_score(dpg.get_value(timer_display_tag), gear)
    else:
        Control._save_deployment_gear_score("EightySix", gear)


# -----------------------------------------------------------------------------------------
def reset_timer():
    global timer_running, elapsed_time
    timer_running = False
    elapsed_time = 0
    dpg.set_value(timer_display_tag, "00:00:00.000")


# -----------------------------------------------------------------------------------------
# FIX: do NOT close/terminate audio here (UI thread). Only signal the worker to stop.
def stop_training_early():
    global timer_running, elapsed_time, session_active, manual_ready, manual_stop, manual_eighty_six

    timer_running = False
    elapsed_time = 0
    dpg.set_value(timer_display_tag, "00:00:00.000")

    # Tell the listening thread to exit ASAP
    session_active = False

    # Clear any manual flags
    manual_ready = False
    manual_stop = False
    manual_eighty_six = False

    _hide_manual_stop_button()
    _hide_manual_eighty_six_button()
    _hide_manual_ready_button()
    _reset_rep_counter()
    enable_ui_controls()


# -----------------------------------------------------------------------------------------
def raise_thread_priority():
    try:
        ctypes.windll.kernel32.SetThreadPriority(
            ctypes.windll.kernel32.GetCurrentThread(), 2)
    except Exception as e:
        print("Could not raise thread priority:", e)


# -----------------------------------------------------------------------------------------
def disable_ui_controls():
    dpg.disable_item("start_session_btn")
    dpg.disable_item("reset_btn")
    dpg.disable_item("repetition_input")
    dpg.hide_item("start_session_btn")
    dpg.hide_item("reset_btn")
    dpg.hide_item("repetition_input")
    set_window_closable(False)


# -----------------------------------------------------------------------------------------
def enable_ui_controls():
    dpg.enable_item("start_session_btn")
    dpg.enable_item("reset_btn")
    dpg.enable_item("repetition_input")
    dpg.show_item("start_session_btn")
    dpg.show_item("reset_btn")
    dpg.show_item("repetition_input")
    set_window_closable(True)


# -----------------------------------------------------------------------------------------
def _hide_manual_ready_button():
    if dpg.is_item_shown("manual_ready_btn"):
        dpg.hide_item("manual_ready_btn")


# -----------------------------------------------------------------------------------------
def _hide_manual_stop_button():
    if dpg.is_item_shown("manual_stop_btn"):
        dpg.hide_item("manual_stop_btn")


# -----------------------------------------------------------------------------------------
def _hide_manual_eighty_six_button():
    if dpg.is_item_shown("manual_eighty_six_btn"):
        dpg.hide_item("manual_eighty_six_btn")


# -----------------------------------------------------------------------------------------
def _show_manual_ready_button():
    if not dpg.is_item_shown("manual_ready_btn"):
        dpg.show_item("manual_ready_btn")


# -----------------------------------------------------------------------------------------
def _show_manual_stop_button():
    if not dpg.is_item_shown("manual_stop_btn"):
        dpg.show_item("manual_stop_btn")


# -----------------------------------------------------------------------------------------
def _show_manual_eighty_six_button():
    if not dpg.is_item_shown("manual_eighty_six_btn"):
        dpg.show_item("manual_eighty_six_btn")


# -----------------------------------------------------------------------------------------
def set_window_closable(state: bool):
    dpg.configure_item("tag_timer", no_title_bar=not state)


# -----------------------------------------------------------------------------------------
def _update_rep_counter(repCount: int):
    global repetitions
    dpg.set_value("rep_count_txt", f"{rep_count_default_text} " + str(repCount) + "/" + str(repetitions))


# -----------------------------------------------------------------------------------------
def _reset_rep_counter():
    global rep_count_default_text
    dpg.set_value("rep_count_txt", rep_count_default_text)


# -----------------------------------------------------------------------------------------
def listen_for_commands():
    global current_round, repetitions, session_active, manual_ready, manual_stop, manual_eighty_six, stream, mic

    raise_thread_priority()
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=1024)
    stream.start_stream()
    recognizer = KaldiRecognizer(vosk_model, 16000)

    try:
        while current_round < repetitions:

            # If user stopped training early, exit cleanly
            if not session_active:
                break

            # Cleaning to prevent next recog. misinterpretation.
            recognizer.Reset()

            Control.play_sound("assets/audio/ready.wav", True)
            _show_manual_ready_button()

            # -------------------- READY LISTEN LOOP --------------------
            while True:
                if not session_active:
                    break

                try:
                    data = stream.read(1024, exception_on_overflow=False)
                except OSError:
                    # Stream closed during shutdown
                    session_active = False
                    break

                # Get text from either final or partial result
                if recognizer.AcceptWaveform(data):
                    result_json = json.loads(recognizer.Result())
                    speech = result_json.get("text", "").strip().lower()
                else:
                    result_json = json.loads(recognizer.PartialResult())
                    speech = result_json.get("partial", "").strip().lower()

                # Manual override
                if manual_ready:
                    _hide_manual_ready_button()
                    manual_ready = False  # to reset
                    Control.play_sound("assets/audio/tenfour.wav", True)
                    break

                if not speech:
                    continue

                words = speech.split()

                # "ready" as a word anywhere in the text
                if "ready" in words:
                    _hide_manual_ready_button()
                    manual_ready = False  # to reset
                    Control.play_sound("assets/audio/tenfour.wav", True)
                    break

            if not session_active:
                break

            delay = random.randint(1, 20)

            # So timer can make sound every second
            for i in range(delay):
                if not session_active:
                    break
                Control.play_sound("assets/audio/ui_sound_04.wav", wait=False)
                time.sleep(1)

            if not session_active:
                reset_timer()
                break

            reset_timer()
            Control.play_sound("assets/audio/deploy.wav", wait=False)
            start_timer()
            _show_manual_stop_button()
            _show_manual_eighty_six_button()

            # Cleaning to prevent next recog. misinterpretation.
            recognizer.Reset()

            # -------------------- STOP/EIGHTY-SIX LISTEN LOOP --------------------
            while True:
                if not session_active:
                    break

                try:
                    data = stream.read(1024, exception_on_overflow=False)
                except OSError:
                    # Stream closed during shutdown
                    session_active = False
                    break

                # Get text from either final or partial result
                if recognizer.AcceptWaveform(data):
                    result_json = json.loads(recognizer.Result())
                    speech = result_json.get("text", "").strip().lower()
                else:
                    result_json = json.loads(recognizer.PartialResult())
                    speech = result_json.get("partial", "").strip().lower()

                # Manual overrides always win
                if manual_stop:
                    manual_stop = False  # resets value immediately
                    stop_timer_internal()
                    _hide_manual_stop_button()
                    _hide_manual_eighty_six_button()
                    current_round += 1
                    Control.play_sound("assets/audio/heard.wav")
                    _update_rep_counter(current_round)
                    break

                if manual_eighty_six:
                    manual_eighty_six = False  # resets value immediately
                    stop_timer_internal(eighty_six=True)
                    _hide_manual_stop_button()
                    _hide_manual_eighty_six_button()
                    Control.play_sound("assets/audio/heard.wav")
                    break

                if not speech:
                    continue

                words = speech.split()

                # --- STOP detection: "stop" as a word anywhere ---
                if "stop" in words:
                    stop_timer_internal()
                    _hide_manual_stop_button()
                    _hide_manual_eighty_six_button()
                    current_round += 1
                    Control.play_sound("assets/audio/heard.wav")
                    _update_rep_counter(current_round)
                    break

                # --- EIGHTY SIX detection ---
                # 1) phrase "eighty six" anywhere
                # 2) numeric "86" as a word
                # 3) "eighty" as a word (first-part shortcut)
                if (
                        "eighty six" in speech
                        or "86" in words
                        or "eighty" in words
                ):
                    stop_timer_internal(eighty_six=True)
                    _hide_manual_stop_button()
                    _hide_manual_eighty_six_button()
                    Control.play_sound("assets/audio/heard.wav")
                    break

            if not session_active:
                reset_timer()
                break

    finally:
        # FIX: audio cleanup happens ONLY here, in the worker thread.
        try:
            if stream is not None:
                try:
                    if stream.is_active():
                        stream.stop_stream()
                except Exception:
                    pass
                try:
                    stream.close()
                except Exception:
                    pass
            if mic is not None:
                try:
                    mic.terminate()
                except Exception:
                    pass
        except Exception:
            pass

    # If we stopped early, don't play "training complete"
    if session_active:
        Control.play_sound("assets/audio/training_complete.wav")

    session_active = False
    _reset_rep_counter()
    enable_ui_controls()


# -----------------------------------------------------------------------------------------
def start_session_callback():
    global current_round, repetitions, session_active
    if session_active:
        return
    current_round = 0
    repetitions = int(dpg.get_value("repetition_input"))
    session_active = True
    disable_ui_controls()
    threading.Thread(target=listen_for_commands, daemon=True).start()


# -----------------------------------------------------------------------------------------
def _manual_ready_callback():
    global manual_ready
    manual_ready = True
    _hide_manual_ready_button()


# -----------------------------------------------------------------------------------------
def _manual_stop_callback():
    global manual_stop
    manual_stop = True
    _hide_manual_stop_button()


# -----------------------------------------------------------------------------------------
def _manual_eighty_six_callback():
    global manual_eighty_six
    manual_eighty_six = True
    _hide_manual_eighty_six_button()


# -----------------------------------------------------------------------------------------
def show_timer(sender, app_data, user_data):
    global gear, rep_count_default_text
    gear = user_data[0]
    previous_window = user_data[1]
    window_tag = "tag_timer"

    Control._check_window_exists(window_tag)

    dpg.hide_item(previous_window)

    Control.play_sound("assets/audio/ui_sound_01.wav", wait=False)

    with dpg.window(label="Timer", tag=window_tag, width=445, height=570, no_title_bar=False, no_move=True,
                    on_close=lambda: (Control._show_window(previous_window),
                                      Control.play_sound("assets/audio/ui_sound_05.wav", wait=False),
                                      Control._delete_window(window_tag))):
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=150)
            dpg.add_text(rep_count_default_text, tag="rep_count_txt")

        dpg.add_text("00:00:00.000", tag=timer_display_tag)
        dpg.add_spacer(height=10)

        # === Parent Window Theme ===
        with dpg.theme() as parent_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                # Transparent window background
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 50))
                # Title bar background (normal and active)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0, 0, 0, 250))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (0, 0, 0, 250))
                # Optional: border color (dark grey)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (20, 20, 20, 150))
        # === Button Themes ===
        with dpg.theme() as red_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))  # Bright red active
        with dpg.theme() as red_int_button_theme:
            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))  # Bright red active

        with dpg.group(horizontal=True):
            dpg.add_button(label="Reset", callback=reset_timer, tag="reset_btn")
            dpg.add_button(label="Stop Training (No Log)", callback=stop_training_early, tag="stop_session_btn")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Manual-Ready", show=False, callback=_manual_ready_callback, width=160, height=80,
                           tag="manual_ready_btn")
            dpg.add_button(label="Manual-Stop", show=False, callback=_manual_stop_callback, width=160, height=80,
                           tag="manual_stop_btn")
            dpg.add_button(label="Manual-EightySix", show=False, callback=_manual_eighty_six_callback, width=160,
                           height=80, tag="manual_eighty_six_btn")

        dpg.add_spacer(height=10)
        dpg.add_input_int(label="Repetitions (N)", default_value=1, tag="repetition_input", min_value=1)
        dpg.add_button(label="Start Session", callback=start_session_callback, tag="start_session_btn")

        dpg.bind_item_theme("reset_btn", red_button_theme)
        dpg.bind_item_theme("manual_ready_btn", red_button_theme)
        dpg.bind_item_theme("manual_stop_btn", red_button_theme)
        dpg.bind_item_theme("manual_eighty_six_btn", red_button_theme)
        dpg.bind_item_theme("start_session_btn", red_button_theme)
        dpg.bind_item_theme("stop_session_btn", red_button_theme)
        dpg.bind_item_theme("repetition_input", red_int_button_theme)

    dpg.focus_item(window_tag)
    dpg.bind_item_theme(window_tag, parent_theme)
