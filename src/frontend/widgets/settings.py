import attrs
import logging
from weakref import WeakValueDictionary
from peewee import fn
from typing import Optional

# from soloviy.models import dbmodels
from src.config import settings
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QMainWindow, QDialog
from dynaconf.loaders.toml_loader import write
from src.frontend.ui.ui_settings import Ui_Form


logger = logging.getLogger(__name__)


@attrs.define
class Settings(QDialog, Ui_Form):
    parent: QMainWindow

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.__attrs_init__(parent)

    def __attrs_pre_init__(self):
        self.setupUi(self)

    @staticmethod
    def persist_settings():
        logger.info("Persisted settings")
        data = settings.as_dict()
        write(settings.settings_file, data)
