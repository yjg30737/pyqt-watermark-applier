import datetime

from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices

from script import get_version


import os

from qtpy.QtGui import QPainter
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtWidgets import QLabel

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
        filename = os.path.join(os.path.dirname(__file__), filename)
        self.__renderer = QSvgRenderer(filename)
        self.resize(self.__renderer.defaultSize())
        length = max(self.sizeHint().width(), self.sizeHint().height())
        self.setFixedSize(length, length)


class ClickableLabel(SvgLabel):
    def __init__(self):
        super().__init__()
        self.__url = '127.0.0.1'

    def setUrl(self, url):
        self.__url = url

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            QDesktopServices.openUrl(QUrl(self.__url))


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("About")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        logoImg = QLabel()
        logoImg.setPixmap(QPixmap("yjgsoft_logo.png"))

        descWidget1 = QLabel()
        descWidget1.setText(f'''
                <h1>Watermark Applier</h1>
                Software Version {get_version()}<br/><br/>
                © 2023-{datetime.datetime.now().year} Used under the MIT License.<br/> 
                Copyright (c) {datetime.datetime.now().year} YJGSoft.<br/>
''')

        descWidget2 = QLabel()
        descWidget2.setText(f'''
                Contact: yjg30737@gmail.com<br/>
                <p>Powered by PyQt5</p>
                ''')

        descWidget1.setAlignment(Qt.AlignTop)
        descWidget2.setAlignment(Qt.AlignTop)

        self.__githubLbl = ClickableLabel()
        self.__githubLbl.setSvgFile('ico/github.svg')
        self.__githubLbl.setUrl('https://github.com/yjg30737/pyqt-openai')
        self.__githubLbl.setFixedSize(22, 22)

        self.__discordLbl = ClickableLabel()
        self.__discordLbl.setSvgFile('ico/discord.svg')
        self.__discordLbl.setUrl('https://discord.gg/cHekprskVE')
        self.__discordLbl.setFixedSize(22, 19)

        lay = QHBoxLayout()
        lay.addWidget(self.__githubLbl)
        lay.addWidget(self.__discordLbl)
        lay.setAlignment(Qt.AlignLeft)
        lay.setContentsMargins(0, 0, 0, 0)

        linkWidget = QWidget()
        linkWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(descWidget1)
        lay.addWidget(descWidget2)
        lay.addWidget(linkWidget)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(logoImg)
        lay.addWidget(rightWidget)

        self.setLayout(lay)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = AboutDialog()
    w.show()
    sys.exit(app.exec())