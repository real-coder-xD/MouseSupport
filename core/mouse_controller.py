from .scroll_manager import set_scroll_direction
from .scroll_manager import set_scroll_active
from pynput.mouse import Listener, Button
from pynput.keyboard import Controller, Key

# Khởi tạo keyboard controller
keyboard = Controller()


def on_click(x, y, button, pressed):
    if button == Button.x1:
        if pressed:
            set_scroll_active(True)
            set_scroll_direction(-1)  # Scroll down
        else:
            set_scroll_active(False)
            set_scroll_direction(0)
    elif button == Button.x2:
        if pressed:
            set_scroll_active(True)
            set_scroll_direction(1)  # Scroll up
        else:
            set_scroll_active(False)
            set_scroll_direction(0)
    elif button == Button.middle and pressed:
        # Gửi phím F9 khi nhấn chuột giữa
        keyboard.press(Key.f9)
        keyboard.release(Key.f9)
    return True


def start_listener():
    listener = Listener(on_click=on_click)
    listener.start()
    return listener