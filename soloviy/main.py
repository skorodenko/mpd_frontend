import sys
import qtinter
from soloviy import resources_rc
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import (
    QQmlApplicationEngine,
    qmlRegisterType,
    qmlRegisterSingletonInstance,
)
# from soloviy.config import settings


if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load(QUrl.fromLocalFile(":/Root.qml"))

    if len(engine.rootObjects()) == 0:
        quit()

    with qtinter.using_asyncio_from_qt():
        sys.exit(app.exec())
