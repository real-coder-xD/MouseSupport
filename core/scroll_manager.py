from pynput.mouse import Controller
import threading
import time

mouse_controller = Controller()
stop_flag = threading.Event()

scroll_active = False
scroll_direction = 0
scroll_delay = 0.01


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
    stop_flag.set()


def auto_scroll():
    while not stop_flag.is_set():
        if scroll_active and scroll_direction != 0:
            mouse_controller.scroll(0, scroll_direction)
        time.sleep(scroll_delay)
