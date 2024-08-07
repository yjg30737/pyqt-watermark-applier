import os

from PySide6.QtGui import QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLabel

from constants import SRC_DIR


class SvgLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.__renderer = ''

    def paintEvent(self, e):
        painter = QPainter(self)
        if self.__renderer:
            self.__renderer.render(painter)
        return super().paintEvent(e)

    def setSvgFile(self, filename: str):
        filename = os.path.join(SRC_DIR, filename)
        self.__renderer = QSvgRenderer(filename)
        self.resize(self.__renderer.defaultSize())
        length = max(self.sizeHint().width(), self.sizeHint().height())
        self.setFixedSize(length, length)