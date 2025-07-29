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
timer_display_tag = "timer_display"
gear = ""
repetitions = 1
current_round = 0

# Load Vosk model (once)
vosk_model = VoskModel("vosk-model-small-en-us-0.15")

# Initialize mixer only once
pygame.mixer.init()

def play_sound(filename, wait=True):
    full_path = os.path.abspath(filename)
    if not os.path.isfile(full_path) or os.path.getsize(full_path) == 0:
        print(f"[Sound Error] File missing or empty: {full_path}")
        return

    print(f"Playing: {full_path}")
    try:
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
        if wait:
            # Hold the program until sound finishes playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)
    except Exception as e:
        print("Audio playback failed:", e)


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

def stop_timer_internal():
    global timer_running
    timer_running = False
    Model.save_deployment_gear_time(dpg.get_value(timer_display_tag), f"{gear}")

def reset_timer():
    global timer_running, start_time, elapsed_time
    timer_running = False
    elapsed_time = 0
    dpg.set_value(timer_display_tag, "00:00:00.000")

def raise_thread_priority():
    try:
        ctypes.windll.kernel32.SetThreadPriority(
            ctypes.windll.kernel32.GetCurrentThread(), 2  # THREAD_PRIORITY_HIGHEST
        )
        print("Thread priority raised.")
    except Exception as e:
        print("Could not raise thread priority:", e)

def listen_for_commands():
    global current_round, repetitions

    raise_thread_priority()  # Windows only

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                      frames_per_buffer=1024)
    stream.start_stream()

    recognizer = KaldiRecognizer(vosk_model, 16000)

    while current_round < repetitions:
        print(f"[ROUND {current_round+1}/{repetitions}] Say 'ready' to begin...")
        play_sound("assets/audio/ready.wav")

        # Wait for "ready"
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result.get("text") == "ready":
                    play_sound("assets/audio/tenfour.wav")
                    break

        delay = random.randint(0, 20)
        print(f"Starting timer in {delay} seconds...")
        time.sleep(delay)
        reset_timer()
        play_sound("assets/audio/deploy.wav", wait=False)
        start_timer()

        print("Say 'stop' to stop the timer.")
        recognizer.Reset()  # flush anything previously captured

        stop_detected = False
        while not stop_detected:
            data = stream.read(1024, exception_on_overflow=False)

            if recognizer.AcceptWaveform(data):
                continue  # skip full results

            partial = json.loads(recognizer.PartialResult())
            speech = partial.get("partial", "").strip()

            if speech.endswith("stop") or speech == "stop":
                stop_timer_internal()
                current_round += 1
                stop_detected = True
                play_sound("assets/audio/heard.wav")


    stream.stop_stream()
    stream.close()
    mic.terminate()

    print("All repetitions completed.")
    play_sound("assets/audio/training_complete.wav")

def start_session_callback():
    global current_round, repetitions
    current_round = 0
    repetitions = int(dpg.get_value("repetition_input"))
    threading.Thread(target=listen_for_commands, daemon=True).start()

def show_timer(sender, app_data, user_data):
    global gear
    gear = user_data

    if dpg.does_item_exist("tag_timer"):
        dpg.delete_item("tag_timer")

    with dpg.window(label="Timer", modal=True, tag="tag_timer", width=410, height=500,
                    on_close=lambda: dpg.delete_item("tag_timer")):

        dpg.add_text("00:00:00.000", tag=timer_display_tag)
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Reset", callback=reset_timer)

        dpg.add_spacer(height=10)
        dpg.add_input_int(label="Repetitions (N)", default_value=1, tag="repetition_input", min_value=1)
        dpg.add_button(label="Start Session (Voice-Controlled)", callback=start_session_callback)

    dpg.focus_item("tag_timer")
