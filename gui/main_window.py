from core.scroll_manager import update_scroll_delay
from core.scroll_manager import get_scroll_delay
from core.scroll_manager import stop_auto_scroll
from core.mouse_controller import start_listener
from core.scroll_manager import auto_scroll

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFontDatabase, QFont
from pynput import keyboard
import threading
import sys

from core.tray_manager import TrayManager


class MouseSupport(QMainWindow):
    speed_changed = pyqtSignal(float)
    exit_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.font = None
        self.drag_pos = None
        self.listener = None
        self.speed_label = None
        self.tray_manager = None
        self.speed_slider = None
        self.scroll_thread = None
        self.switch_window = False
        self.keyboard_listener = None
        self.exit_requested.connect(self.close)
        self.setup_global_hotkey()
        self.setup_mouse_thread()
        self.setup_tray()

        self.init_ui()

        self.show()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setGeometry(100, 100, 300, 130)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 220);
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 2px;
            }
        """)

        frame_layout = QVBoxLayout(frame)

        frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.setContentsMargins(15, 15, 15, 15)

        font = self.load_font()

        title_label = QLabel("Mouse controller")
        title_label.setFont(font)
        title_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 255, 0, 150);
                font-weight: bold;
                font-size: 20px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(title_label)

        current_delay = get_scroll_delay()
        slider_value = self.delay_to_slider_value(current_delay)

        self.speed_label = QLabel(f"Speed: {1 / current_delay:.1f} scrolls/sec")
        self.speed_label.setFont(font)
        self.speed_label.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 0, 180);
                font-size: 14px;
            }
        """)
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(self.speed_label)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(5)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setValue(slider_value)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(100, 100, 100, 150);
                border-radius: 3px;
                height: 6px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5CBF60, stop:1 #55b059);
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                border-radius: 2px;
            }
        """)
        frame_layout.addWidget(self.speed_slider)

        instruction_label = QLabel("X1: Scroll Down | X2: Scroll Up")
        instruction_label.setFont(font)
        instruction_label.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 200, 200);
                font-size: 12px;
            }
        """)
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(instruction_label)

        hotkey_label = QLabel("Global Hotkey: ALT+Q (Show/Hide)")
        hotkey_label.setFont(font)
        hotkey_label.setStyleSheet("""
            QLabel {
                color: rgba(180, 0, 0, 150);
                font-size: 12px;
            }
        """)
        hotkey_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(hotkey_label)

        layout.addWidget(frame)

        self.drag_pos = None
        self.setMouseTracking(True)
        self.speed_changed.connect(self.update_speed_label)

    def delay_to_slider_value(self, delay):
        if delay <= 0.005:
            return 200
        elif delay >= 0.2:
            return 5
        else:
            self.slider_value = 5 + (0.2 - delay) * 975
            return int(self.slider_value)

    def slider_value_to_delay(self, slider_value):
        self.delay = 0.2 - (slider_value - 5) * (0.195 / 195)
        return max(0.005, min(0.2, self.delay))

    def load_font(self):
        font_path = "fonts/tektur.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                self.font = QFont(font_families[0], 10)
            else:
                self.font = QFont("Arial", 10)
        else:
            self.font = QFont("Arial", 10)
        return self.font

    def on_speed_changed(self, slider_value):
        new_delay = self.slider_value_to_delay(slider_value)

        update_scroll_delay(new_delay)
        self.speed_changed.emit(new_delay)

    def update_speed_label(self, delay):
        if delay > 0:
            scrolls_per_sec = 1 / delay
            self.speed_label.setText(f"Speed: {scrolls_per_sec:.1f} scrolls/sec")

    def setup_mouse_thread(self):
        self.listener = start_listener()
        self.scroll_thread = threading.Thread(target=auto_scroll, daemon=True)
        self.scroll_thread.start()

    def setup_global_hotkey(self):
        def on_activate():
            if self.switch_window:
                self.show_window_from_tray()
                self.switch_window = False
            else:
                self.hide_window_from_tray()
                self.switch_window = True

        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<ALT>+Q'),
            on_activate
        )

        def for_canonical(f):
            return lambda k: f(self.keyboard_listener.canonical(k))

        def start_keyboard_listener():
            with keyboard.Listener(
                    on_press=for_canonical(hotkey.press),
                    on_release=for_canonical(hotkey.release)
            ) as listener:
                self.keyboard_listener = listener
                listener.join()

        keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
        keyboard_thread.start()

    def setup_tray(self):
        self.tray_manager = TrayManager("Mouse controller")
        self.tray_manager.show_window_requested.connect(self.show_window_from_tray)
        self.tray_manager.hide_window_requested.connect(self.hide_window_from_tray)
        self.tray_manager.exit_requested.connect(self.exit_application)
        self.tray_manager.setup_tray()

    def show_window_from_tray(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def hide_window_from_tray(self):
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def exit_application(self):
        if self.listener:
            self.listener.stop()

        if self.keyboard_listener:
            self.keyboard_listener.stop()

        if self.tray_manager:
            self.tray_manager.stop()

        stop_auto_scroll()
        QApplication.quit()
        sys.exit()
