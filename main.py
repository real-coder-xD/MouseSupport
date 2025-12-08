from gui.main_window import TransparentWindow
from PyQt6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Mouse scroll controller")

    TransparentWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
