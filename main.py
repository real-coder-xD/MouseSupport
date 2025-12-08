from gui.main_window import MouseSupport
from PyQt6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Mouse controller")

    MouseSupport()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
