from PyQt6.QtWidgets import QApplication

from hyperart_gui import HyperArtWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = HyperArtWindow()
    window.show()
    sys.exit(app.exec())
