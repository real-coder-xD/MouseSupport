from .scroll_manager import set_scroll_direction
from .scroll_manager import set_scroll_active

from pynput.mouse import Listener
from pynput.mouse import Button
from pynput.keyboard import Key

import pynput

keyboard = pynput.keyboard.Controller()
mouse =  pynput.mouse.Controller()

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

    if button == Button.middle and pressed:
        mouse.click(Button.left)
        keyboard.press(Key.f9)
        keyboard.release(Key.f9)
    return True


def start_listener():
    listener = Listener(on_click=mouse_click)
    listener.start()
    return listener