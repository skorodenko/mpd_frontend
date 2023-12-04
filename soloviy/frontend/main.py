import sys
import qtinter
from PySide6.QtWidgets import QApplication
from soloviy.frontend.widgets.main_window import MainWindow
from soloviy.config import settings


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with qtinter.using_asyncio_from_qt():
        main_window = MainWindow()
        main_window.serve()
        app.exec()