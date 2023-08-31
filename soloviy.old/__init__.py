import sys
import qtinter
from PyQt6.QtWidgets import QApplication
from soloviy.widgets.main import MainWindow


def main():
    app = QApplication(sys.argv)
    with qtinter.using_asyncio_from_qt():
        main_window = MainWindow()
        main_window.serve()
        app.exec()
