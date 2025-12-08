from .scroll_manager import set_scroll_direction
from .scroll_manager import set_scroll_active

from pynput.mouse import Listener
from pynput.mouse import Button


def start_listener():
    def on_click(x, y, button, pressed):
        if pressed:
            if button == mouse.Button.x1:
                set_scroll_direction(-1)
                set_scroll_active(True)
            elif button == mouse.Button.x2:
                set_scroll_direction(1)
                set_scroll_active(True)
        else:
            set_scroll_active(False)

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    return listener


def on_click(x, y, button, pressed):
    if button == Button.x1:
        if pressed:
            set_scroll_active(True)
            set_scroll_direction(-10)
        else:
            set_scroll_active(False)
            set_scroll_direction(0)
    elif button == Button.x2:
        if pressed:
            set_scroll_active(True)
            set_scroll_direction(10)
        else:
            set_scroll_active(False)
            set_scroll_direction(0)
    return True


def start_listener():
    listener = Listener(on_click=on_click)
    listener.start()
    return listener
