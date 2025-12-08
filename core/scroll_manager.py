from pynput.mouse import Controller
import time


stop_scroll_thread = False
scroll_active = False
scroll_direction = 0
scroll_delay = 0.02

mouse_controller = Controller()

def update_scroll_delay(new_delay):
    global scroll_delay
    scroll_delay = new_delay

def get_scroll_delay():
    return scroll_delay

def set_scroll_direction(direction):
    global scroll_direction
    scroll_direction = direction

def get_scroll_direction():
    return scroll_direction

def set_scroll_active(active):
    global scroll_active
    scroll_active = active

def get_scroll_active():
    return scroll_active

def stop_auto_scroll():
    global stop_scroll_thread
    stop_scroll_thread = True

def auto_scroll():
    global stop_scroll_thread
    while not stop_scroll_thread:
        if scroll_active and scroll_direction != 0:
            mouse_controller.scroll(0, scroll_direction)
        time.sleep(scroll_delay)
