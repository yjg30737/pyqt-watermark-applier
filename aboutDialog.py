import datetime

from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices

from script import get_version


# class ClickableLabel(SvgLabel):
#     def __init__(self):
#         super().__init__()
#         self.__url = '127.0.0.1'
#
#     def setUrl(self, url):
#         self.__url = url
#
#     def mouseReleaseEvent(self, QMouseEvent):
#         if QMouseEvent.button() == Qt.LeftButton:
#             QDesktopServices.openUrl(QUrl(self.__url))


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
                <h1>pyqt-openai</h1>
                Software Version {get_version()}<br/><br/>
                © 2023 {datetime.datetime.now().year}. Used under the MIT License.<br/>
                Copyright (c) {datetime.datetime.now().year} yjg30737<br/>
                ''')

        descWidget2 = QLabel()
        descWidget2.setText('Read MIT License Full Text')
        descWidget2.setUrl('https://github.com/yjg30737/pyqt-openai/blob/main/LICENSE')
        descWidget2.setStyleSheet('QLabel:hover { color: blue }')

        descWidget3 = QLabel()
        descWidget3.setText(f'''
                <br/><br/>Contact: yjg30737@gmail.com<br/>
                <p>Powered by PyQt5</p>
                ''')

        descWidget1.setAlignment(Qt.AlignTop)
        descWidget2.setAlignment(Qt.AlignTop)
        descWidget3.setAlignment(Qt.AlignTop)

        self.__githubLbl = QLabel()
        self.__githubLbl.setUrl('https://github.com/yjg30737/pyqt-openai')

        self.__discordLbl = QLabel()
        self.__discordLbl.setUrl('https://discord.gg/cHekprskVE')

        lay = QHBoxLayout()
        lay.addWidget(logoImg)
        lay.addWidget(QLabel("This is a simple watermark applier using PyQt5"))

        self.setLayout(lay)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = AboutDialog()
    w.show()
    sys.exit(app.exec())