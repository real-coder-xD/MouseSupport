from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject
from PIL import ImageDraw
from PIL import Image
import threading
import pystray
import sys
import os


class TrayManager(QObject):
    show_window_requested = pyqtSignal()
    hide_window_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, app_name, parent=None):
        super().__init__(parent)
        self.app_name = app_name
        self.tray_icon = None
        self.tray_thread = None
        self.is_running = False

    def setup_tray(self, icon_path=None):
        icon_image = self.load_icon(icon_path)

        menu = pystray.Menu(
            pystray.MenuItem(" Show Window ", self.show_window),
            pystray.MenuItem(" Hide Window ", self.hide_window),
            pystray.MenuItem(" Exit Window ", self.exit_app)
        )

        self.tray_icon = pystray.Icon(
            self.app_name,
            icon_image,
            self.app_name,
            menu
        )

        self.is_running = True
        self.tray_thread = threading.Thread(target=self.run_tray, daemon=True)
        self.tray_thread.start()

    def load_icon(self, icon_path=None):
        possible_paths = [
            "icons/icon.png",
        ]

        for path in possible_paths:
            if path and os.path.exists(path):
                try:
                    return Image.open(path)
                except Exception as e:
                    continue

    def show_window(self, icon, item):
        self.show_window_requested.emit()

    def hide_window(self, icon, item):
        self.hide_window_requested.emit()

    def exit_app(self, icon, item):
        self.exit_requested.emit()

    def run_tray(self):
        if self.tray_icon:
            self.tray_icon.run()

    def stop(self):
        self.is_running = False
        if self.tray_icon:
            self.tray_icon.stop()
