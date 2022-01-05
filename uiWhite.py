# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush, QColor,QSyntaxHighlighter,QTextCharFormat, QConicalGradient, QCursor,QTextFormat, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QTextEdit
from PyQt5.QtCore import QCoreApplication,QRegExp, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent
from White_ import Ui_uiMainWindow
import sys
from Ui_function import *
import platform

class uimain_white(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_uiMainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setGeometry(QtCore.QRect(180, 270, 75, 23))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("python.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(22, 22))
        self.pushButton.setObjectName("pushButton")
        self.ui.actionAdd_Tab.triggered.connect(self.add)
        self.ui.statusbar.showMessage("Pycos Visual")
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.statusbar.addPermanentWidget(self.pushButton)
        self.ui.pushButton_6.clicked.connect(self.close)
        self.ui.pushButton_7.clicked.connect(self.showMinimized)
        self.ui.pushButton_5.clicked.connect(self.showMaximized)
        self.ui.pushButton_8.clicked.connect(self.showNormal)
        self.ui.actionOpen_File_Ctrl_N.triggered.connect(self.add)
        self.ui.actionEdit.triggered.connect(self.theme)
        def moveWindow(event):
                    # RESTORE BEFORE MOVE

                    # IF LEFT CLICK MOVE WINDOW
                    if event.buttons() == Qt.LeftButton:
                        self.move(self.pos() + event.globalPos() - self.dragPos)
                        self.dragPos = event.globalPos()
                        event.accept()

                # SET TITLE BAR
        self.ui.frame_3.mouseMoveEvent = moveWindow
        UIFunctions.uiDefinitions(self)
    def add(self):
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setStyleSheet("background:#ebebeb;")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_5.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.plainTextEdit = QTextEdit(self.tab_3)
        self.plainTextEdit.ExtraSelection()
        self.plainTextEdit.setStyleSheet("\n"
"background:#ebebeb;\n"
"border-style: 0px;\n"
"font-family: consolas;\n"
"color: black;\n"
"font-size: 16px;\n"
"\n"
"QScrollBar::sub-page:vertical {\n"
"background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical {\n"
"background:none;\n"
"}\n"
"QScrollBar:vertical {\n"
"            border: 0px solid #999999;\n"
"            background: rgb(0, 13, 26);\n"
"            width:10px;    \n"
"            margin: 0px 0px 0px 0px;\n"
"            border-radius: 4px;\n"
"        }\n"
"        QScrollBar::handle:vertical {         \n"
"       \n"
"            min-height: 0px;\n"
"              border: 0px solid red;\n"
"            border-radius: 4px;\n"
"            \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
"        }\n"
"        QScrollBar::add-line:vertical {       \n"
"            height: 0px;\n"
"            subcontrol-position: bottom;\n"
"            subcontrol-origin: margin;\n"
"        }\n"
"        QScrollBar::sub-line:vertical {\n"
"            height: 0 px;\n"
"            subcontrol-position: top;\n"
"            subcontrol-origin: margin;\n"
"        }\n"
"")
        extraSelections = []
        self.plainTextEdit.setLineWidth(18)
        self.plainTextEdit.setMidLineWidth(18)
        self.plainTextEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.plainTextEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_5.addWidget(self.plainTextEdit)
        self.ui.tabWidget.addTab(self.tab_3, "Files")
        qfd = QFileDialog()
        path = "D:\ennine\SIG HTB\BGN"
        filter = "py(*.py)"
        filename = QtWidgets.QFileDialog.getOpenFileName()

        if filename[0]:
            f = open(filename[0], 'r', encoding="utf8")
        with f:
            data = f.read()
            self.plainTextEdit.setPlainText(data)
    def mousePressEvent(self, event):
            self.dragPos = event.globalPos()
    def close_tab(self,index):
          self.ui.tabWidget.removeTab(index)
    def theme(self):
        from Maintheme import ui_Uimain
        self.theme_ = ui_Uimain()
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = uimain()
    sys.exit(app.exec_())
