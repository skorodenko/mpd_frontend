import os
import sys
import qasync
import signal
import asyncio
import subprocess
from time import sleep
import src.ui.resources_rc
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
# from soloviy.config import settings

def runner():
    try:
        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
            os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"
        
        engine = QQmlApplicationEngine()
        engine.addImportPath("/home/rinkuro/Sandbox/Soloviy/src/ui/qml")
        
        #server = subprocess.Popen(["python", "-m", "src.service.run"])
        #sleep(2)
        
        engine.load(QUrl.fromLocalFile(":/Root.qml"))
        engine.quit.connect(app.quit)
        engine.quit.connect(loop.close)
        
        with loop:
            loop.run_forever()
    
    except Exception:
        ...
    
    finally:   
        #try:
        #    server.wait(2)   
        #except subprocess.TimeoutExpired:
        #    server.kill()
        ...
        

if __name__ == "__main__":
    runner()