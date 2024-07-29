import datetime
import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QWidget, QVBoxLayout

from constants import COMPANY_LOGO, APP_NAME, LICENSE, __author__, __version__, FRAMEWORK, CONTACT, ICON_DISCORD, \
    ICON_GITHUB, GITHUB_URL, DISCORD_URL
from widgets.linkLabel import LinkLabel


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
        if QMouseEvent.button() == Qt.MouseButton.LeftButton:
            QDesktopServices.openUrl(QUrl(self.__url))


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("About")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        p = QPixmap(COMPANY_LOGO)
        logoImg = QLabel()
        logoImg.setPixmap(p)

        descWidget1 = QLabel()
        descWidget1.setText(f'''
                <h1>{APP_NAME}</h1>
                Software Version {__version__}<br/><br/>
                © 2023-{datetime.datetime.now().year} Used under the {LICENSE} License.<br/> 
                Copyright (c) {datetime.datetime.now().year} {__author__}.<br/>
''')

        descWidget2 = QLabel()
        descWidget2.setText(f'''
                Contact: {CONTACT}<br/>
                <p>Powered by {FRAMEWORK}</p>
                ''')

        descWidget1.setAlignment(Qt.AlignmentFlag.AlignTop)
        descWidget2.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__githubLbl = ClickableLabel()
        self.__githubLbl.setSvgFile(ICON_GITHUB)
        self.__githubLbl.setUrl(GITHUB_URL)
        self.__githubLbl.setFixedSize(22, 22)

        self.__discordLbl = ClickableLabel()
        self.__discordLbl.setSvgFile(ICON_DISCORD)
        self.__discordLbl.setUrl(DISCORD_URL)
        self.__discordLbl.setFixedSize(22, 19)

        lay = QHBoxLayout()
        lay.addWidget(self.__githubLbl)
        lay.addWidget(self.__discordLbl)
        lay.setAlignment(Qt.AlignmentFlag.AlignLeft)
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