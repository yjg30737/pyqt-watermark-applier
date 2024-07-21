import os, sys

# Get the absolute path of the current script file
from fileListWidget import FindPathWidget
from notifier import NotifierWidget
from script import WatermarkSetter, open_directory
from constants import APP_ICON, EXTENSIONS, DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE

script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidget, QVBoxLayout, QWidget, QGroupBox, \
    QFormLayout, QSpinBox, QCheckBox, QComboBox, QDoubleSpinBox, QSystemTrayIcon, QAction, QMenu, QStyle, QMessageBox, \
    QLineEdit
from PyQt5.QtCore import Qt, QCoreApplication, QThread, QSettings
from PyQt5.QtGui import QFont, QIcon

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont(DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE))


class Thread(QThread):
    def __init__(self, args, watermark_filename, src_dirname, dst_dirname):
        super(Thread, self).__init__()
        self.__thread_args = args
        self.__watermark_filename = watermark_filename
        self.__src_dirname = src_dirname
        self.__dst_dirname = dst_dirname
        self.__setter = WatermarkSetter()

    def run(self):
        try:
            width = self.__thread_args['width']
            height = self.__thread_args['height']
            margin = self.__thread_args['margin']
            position = self.__thread_args['position']
            opacity = self.__thread_args['opacity']
            watermark_type = self.__thread_args['watermark_type']
            src_dirname = self.__src_dirname
            dst_dirname = self.__dst_dirname
            self.__setter.set_watermark(self.__watermark_filename)
            self.__setter.resize_watermark(width, height)
            self.__setter.set_margin(margin)
            self.__setter.set_position(position)
            self.__setter.set_watermark_opacity(opacity)
            self.__setter.set_type(watermark_type)
            self.__setter.apply_watermark_from_directory(src_dirname=src_dirname, dst_dirname=dst_dirname)
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__src_dirname = ''
        self.__dst_dirname = ''
        self.__watermark_filename = ''

        self.__settings_ini = QSettings('settings.ini', QSettings.IniFormat)

        if not self.__settings_ini.contains('opacity'):
            self.__settings_ini.setValue('opacity', 0.0)
        if not self.__settings_ini.contains('margin'):
            self.__settings_ini.setValue('margin', 0)
        if not self.__settings_ini.contains('width'):
            self.__settings_ini.setValue('width', 150)
        if not self.__settings_ini.contains('height'):
            self.__settings_ini.setValue('height', 150)
        if not self.__settings_ini.contains('fix_ratio'):
            self.__settings_ini.setValue('fix_ratio', False)
        if not self.__settings_ini.contains('position'):
            self.__settings_ini.setValue('position', 'bottom right')
        if not self.__settings_ini.contains('watermark_type'):
            self.__settings_ini.setValue('watermark_type', 'normal')

        self.__opacity = self.__settings_ini.value('opacity', type=float)
        self.__margin = self.__settings_ini.value('margin', type=int)
        self.__width = self.__settings_ini.value('width', type=int)
        self.__height = self.__settings_ini.value('height', type=int)
        self.__fix_ratio = self.__settings_ini.value('fix_ratio', type=bool)
        self.__position = self.__settings_ini.value('position', type=str)
        self.__watermark_type = self.__settings_ini.value('watermark_type', type=str)

    def __initUi(self):
        self.setMinimumSize(700, 500)
        self.setWindowTitle('Watermark Applier')
        self.__srcFindPathWidget = FindPathWidget()
        self.__srcFindPathWidget.getLineEdit().setPlaceholderText('Set Directory Including Images...')
        self.__srcFindPathWidget.setAsDirectory(True)
        self.__srcFindPathWidget.added.connect(self.__addToList)

        self.__listWidget = QListWidget()

        # Settings of the watermark file
        self.__watermarkFindPathWidget = FindPathWidget()
        self.__watermarkFindPathWidget.getLineEdit().setPlaceholderText('Choose the watermark file...')
        self.__watermarkFindPathWidget.added.connect(self.__registerWatermarkFilename)

        self.__opacitySpinBox = QDoubleSpinBox()
        self.__opacitySpinBox.setRange(0.0, 1.0)
        self.__opacitySpinBox.setSingleStep(0.01)

        self.__marginSpinBox = QSpinBox()
        self.__marginSpinBox.setRange(0, 50)

        self.__widthSpinBox = QSpinBox()
        self.__widthSpinBox.setRange(0, 1000)

        self.__heightSpinBox = QSpinBox()
        self.__heightSpinBox.setRange(0, 1000)

        self.__fixRatioChkBox = QCheckBox()

        self.__positionCmbBox = QComboBox()
        self.__positionCmbBox.addItems([
            'top left',
            'top right',
            'bottom left',
            'bottom right'
        ])
        self.__watermarkTypeCmbBox = QComboBox()
        self.__watermarkTypeCmbBox.addItems([
            'normal',
            'tiled'
        ])

        self.__opacitySpinBox.setValue(self.__opacity)
        self.__marginSpinBox.setValue(self.__margin)
        self.__widthSpinBox.setValue(self.__width)
        self.__heightSpinBox.setValue(self.__height)
        self.__fixRatioChkBox.setChecked(self.__fix_ratio)
        self.__positionCmbBox.setCurrentText(self.__position)
        self.__watermarkTypeCmbBox.setCurrentText(self.__watermark_type)

        self.__opacitySpinBox.valueChanged.connect(self.__opacityChanged)
        self.__marginSpinBox.valueChanged.connect(self.__marginChanged)
        self.__widthSpinBox.valueChanged.connect(self.__widthChanged)
        self.__heightSpinBox.valueChanged.connect(self.__heightChanged)
        self.__fixRatioChkBox.stateChanged.connect(self.__fixRatioChkBoxChanged)
        self.__positionCmbBox.currentTextChanged.connect(self.__positionCmbBoxChanged)
        self.__watermarkTypeCmbBox.currentTextChanged.connect(self.__watermarkTypeCmbBoxChanged)

        lay = QFormLayout()
        lay.addRow('Watermark File', self.__watermarkFindPathWidget)
        lay.addRow('Opacity', self.__opacitySpinBox)
        lay.addRow('Margin', self.__marginSpinBox)
        lay.addRow('Width', self.__widthSpinBox)
        lay.addRow('Height', self.__heightSpinBox)
        lay.addRow('Fix Ratio', self.__fixRatioChkBox)
        lay.addRow('Position', self.__positionCmbBox)
        lay.addRow('Type of Watermark', self.__watermarkTypeCmbBox)

        watermarkSettingsGrpBox = QGroupBox()
        watermarkSettingsGrpBox.setTitle('Watermark Settings')
        watermarkSettingsGrpBox.setLayout(lay)

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)
        self.__runBtn.setEnabled(False)

        self.__dstFindPathWidget = FindPathWidget()
        self.__dstFindPathWidget.getLineEdit().setPlaceholderText('Choose the destination folder...')
        self.__dstFindPathWidget.setAsDirectory(True)
        self.__dstFindPathWidget.added.connect(self.__registerDstDirname)

        lay = QVBoxLayout()
        lay.addWidget(watermarkSettingsGrpBox)
        lay.addWidget(self.__srcFindPathWidget)
        lay.addWidget(self.__listWidget)
        lay.addWidget(self.__dstFindPathWidget)
        lay.addWidget(self.__runBtn)
        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.__setTrayMenu()
        QApplication.setQuitOnLastWindowClosed(False)

    def __setTrayMenu(self):
        # background app
        menu = QMenu()

        action = QAction("Quit", self)
        action.setIcon(QIcon('ico/close.svg'))

        action.triggered.connect(app.quit)

        menu.addAction(action)

        tray_icon = QSystemTrayIcon(app)
        tray_icon.setIcon(QIcon(APP_ICON))
        tray_icon.activated.connect(self.__activated)

        tray_icon.setContextMenu(menu)

        tray_icon.show()

    def __activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def __addToList(self, dirname):
        self.__listWidget.clear()
        filenames = [os.path.join(dirname, filename) for filename in os.listdir(dirname)]
        filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in EXTENSIONS]
        self.__src_dirname = dirname
        self.__listWidget.addItems(filenames)
        self.__checkRunBtnEnabled()

    def __registerWatermarkFilename(self, filename):
        self.__watermark_filename = filename
        self.__checkRunBtnEnabled()

    def __registerDstDirname(self, dirname):
        self.__dst_dirname = dirname
        self.__checkRunBtnEnabled()

    def __opacityChanged(self, v):
        self.__opacity = v
        self.__settings_ini.setValue('opacity', self.__opacity)

    def __marginChanged(self, v):
        self.__margin = v
        self.__settings_ini.setValue('margin', self.__margin)

    def __widthChanged(self, v):
        self.__width = v
        self.__settings_ini.setValue('width', self.__width)
        if self.__fix_ratio:
            self.__heightSpinBox.setValue(self.__width)

    def __heightChanged(self, v):
        self.__height = v
        self.__settings_ini.setValue('height', self.__height)
        if self.__fix_ratio:
            self.__widthSpinBox.setValue(self.__height)

    def __fixRatioChkBoxChanged(self, v):
        self.__fix_ratio = v
        self.__settings_ini.setValue('fix_ratio', self.__fix_ratio)
        if self.__fix_ratio:
            v = max(self.__widthSpinBox.value(), self.__heightSpinBox.value())
            self.__widthSpinBox.setValue(v)
            self.__heightSpinBox.setValue(v)

    def __positionCmbBoxChanged(self, v):
        self.__position = v
        self.__settings_ini.setValue('position', self.__position)

    def __watermarkTypeCmbBoxChanged(self, v):
        self.__watermark_type = v
        self.__settings_ini.setValue('watermark_type', self.__watermark_type)

    def __checkRunBtnEnabled(self):
        f = self.__watermarkFindPathWidget.getLineEdit().text().strip() != '' \
            and self.__srcFindPathWidget.getLineEdit().text().strip() != '' \
            and self.__dstFindPathWidget.getLineEdit().text().strip() != ''
        self.__runBtn.setEnabled(f)

    def __run(self):
        thread_arg = {
            'opacity': self.__opacity,
            'margin': self.__margin,
            'width': self.__width,
            'height': self.__height,
            'fix_ratio': self.__fix_ratio,
            'position': self.__position,
            'watermark_type': self.__watermark_type,
        }
        self.__t = Thread(thread_arg, self.__watermark_filename, self.__src_dirname, self.__dst_dirname)
        self.__t.started.connect(self.__started)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        print('started')

    def __finished(self):
        if not self.isVisible():
            self.__notifierWidget = NotifierWidget(informative_text='Task Complete', detailed_text='Click this!')
            self.__notifierWidget.show()
            self.__notifierWidget.doubleClicked.connect(self.show)
        else:
            msgBox = QMessageBox.information(self, 'Finished', 'Task Complete')
        open_directory(self.__dst_dirname)

    def closeEvent(self, e):
        reply = QMessageBox.question(self, 'Close Application',
                                     "Would you like to run the application in the background?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            e.accept()
        else:
            QApplication.exit()



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    QApplication.setWindowIcon(QIcon(APP_ICON))
    w = MainWindow()
    w.show()
    sys.exit(app.exec())