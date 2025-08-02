import dearpygui.dearpygui as dpg
import time
import threading
import random
import json
from vosk import Model as VoskModel, KaldiRecognizer
import pyaudio
import Model
import pygame
import os
import ctypes

# Global state
timer_running = False
start_time = 0
elapsed_time = 0
gear = ""
repetitions = 1
current_round = 0
session_active = False
timer_display_tag = "timer_display"

# Load voice model and audio
vosk_model = VoskModel("vosk-model-small-en-us-0.15")
pygame.mixer.init()

def play_sound(filename, wait=True):
    path = os.path.abspath(filename)
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        print(f"[Sound Error] File missing or empty: {path}")
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        if wait:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)
    except Exception as e:
        print("Audio playback failed:", e)

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

def start_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        start_time = time.perf_counter() - elapsed_time
        timer_running = True
        update_timer()

def stop_timer_internal(botched = False):
    global timer_running
    timer_running = False
    if not botched:
        Model.save_deployment_gear_time(dpg.get_value(timer_display_tag), gear)
    else:
        Model.save_deployment_gear_time("botched", gear)

def reset_timer():
    global timer_running, elapsed_time
    timer_running = False
    elapsed_time = 0
    dpg.set_value(timer_display_tag, "00:00:00.000")

def stop_training_early():
    global timer_running, elapsed_time, session_active
    timer_running = False
    elapsed_time = 0
    dpg.set_value(timer_display_tag, "00:00:00.000")
    print("[Notice] Training stopped early (no log).")
    session_active = False
    enable_ui_controls()

def raise_thread_priority():
    try:
        ctypes.windll.kernel32.SetThreadPriority(
            ctypes.windll.kernel32.GetCurrentThread(), 2)
    except Exception as e:
        print("Could not raise thread priority:", e)

def disable_ui_controls():
    dpg.disable_item("start_session_btn")
    dpg.disable_item("reset_btn")
    dpg.disable_item("repetition_input")
    dpg.hide_item("start_session_btn")
    dpg.hide_item("reset_btn")
    dpg.hide_item("repetition_input")
    set_window_closable(False)

def enable_ui_controls():
    dpg.enable_item("start_session_btn")
    dpg.enable_item("reset_btn")
    dpg.enable_item("repetition_input")
    dpg.show_item("start_session_btn")
    dpg.show_item("reset_btn")
    dpg.show_item("repetition_input")
    set_window_closable(True)

def set_window_closable(state: bool):
    dpg.configure_item("tag_timer", no_title_bar=not state)

def listen_for_commands():
    global current_round, repetitions, session_active

    raise_thread_priority()
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=1024)
    stream.start_stream()
    recognizer = KaldiRecognizer(vosk_model, 16000)

    while current_round < repetitions:
        print(f"[ROUND {current_round+1}/{repetitions}] Say 'ready' to begin...")
        play_sound("assets/audio/ready.wav")

        while True:
            data = stream.read(1024, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                if json.loads(recognizer.Result()).get("text") == "ready":
                    play_sound("assets/audio/tenfour.wav")
                    break

        delay = random.randint(1, 20)
        print(f"Starting timer in {delay} seconds...")
                
        #So timer can make sound every second
        for i in range(delay):
            play_sound("assets/audio/ui_sound_04.wav", wait=False)
            time.sleep(1)
            i += 1
            #So timer can be stopped during countdown.
            if session_active == False:
                reset_timer()
                recognizer.Reset()
                stream.stop_stream()
                stream.close()
                mic.terminate()
                return
                
        
        reset_timer()
        play_sound("assets/audio/deploy.wav", wait=False)
        start_timer()

        recognizer.Reset()
        print("Say 'stop' to stop the timer.")
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                continue
            speech = json.loads(recognizer.PartialResult()).get("partial", "").strip()
            if speech.endswith("stop") or speech == "stop":
                stop_timer_internal()
                current_round += 1
                play_sound("assets/audio/heard.wav")
                break
            elif speech.endswith("botch") or speech == "botch":
                stop_timer_internal(botched=True)
                play_sound("assets/audio/heard.wav")
                break

    stream.stop_stream()
    stream.close()
    mic.terminate()

    print("All repetitions completed.")
    play_sound("assets/audio/training_complete.wav")
    session_active = False
    enable_ui_controls()

def start_session_callback():
    global current_round, repetitions, session_active
    if session_active:
        return
    current_round = 0
    repetitions = int(dpg.get_value("repetition_input"))
    session_active = True
    disable_ui_controls()
    threading.Thread(target=listen_for_commands, daemon=True).start()

def show_timer(sender, app_data, user_data):
    global gear
    gear = user_data[0]
    previous_window = user_data[1]
    window_tag = "tag_timer"

    if dpg.does_item_exist(window_tag):
        dpg.delete_item(window_tag)
    
    dpg.hide_item(previous_window)

    play_sound("assets/audio/ui_sound_01.wav", wait=False)

    with dpg.window(label="Timer", tag=window_tag, width=430, height=570, no_title_bar=False, no_move=True, on_close=lambda: (dpg.show_item(previous_window), play_sound("assets/audio/ui_sound_05.wav", wait=False), dpg.delete_item(window_tag))):
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
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active
        with dpg.theme() as red_int_button_theme:
            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 0, 0, 255))  # Dark red hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 0, 0, 255))   # Bright red active


        with dpg.group(horizontal=True):
            dpg.add_button(label="Reset", callback=reset_timer, tag="reset_btn")
            dpg.add_button(label="Stop Training (No Log)", callback=stop_training_early, tag="stop_session_btn")

        dpg.add_spacer(height=10)
        dpg.add_input_int(label="Repetitions (N)", default_value=1, tag="repetition_input", min_value=1)
        dpg.add_button(label="Start Session (Voice-Controlled)", callback=start_session_callback, tag="start_session_btn")
        
        dpg.bind_item_theme("reset_btn", red_button_theme)
        dpg.bind_item_theme("start_session_btn", red_button_theme)
        dpg.bind_item_theme("stop_session_btn", red_button_theme)
        dpg.bind_item_theme("repetition_input", red_int_button_theme)

    dpg.focus_item(window_tag)
    dpg.bind_item_theme(window_tag, parent_theme)

