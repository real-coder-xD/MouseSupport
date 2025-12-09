from .scroll_manager import set_scroll_direction
from .scroll_manager import set_scroll_active
from pynput.keyboard import Controller, Key
from pynput.mouse import Listener, Button

keyboard = Controller()

def mouse_click(x, y, button, pressed):
    if button == Button.x1:
        if pressed:
            set_scroll_active(True)
            set_scroll_direction(-1)
        else:
            set_scroll_active(False)
            set_scroll_direction(0)
    if button == Button.x2:
        if pressed:
            set_scroll_active(True)
            set_scroll_direction(1)
        else:
            set_scroll_active(False)
            set_scroll_direction(0)

    return True


def start_listener():
    listener = Listener(on_click=mouse_click)
    listener.start()
    return listener