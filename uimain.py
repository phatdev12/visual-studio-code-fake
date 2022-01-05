# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush,QFontMetrics,QPen, QColor,QSyntaxHighlighter,QTextCharFormat, QConicalGradient, QCursor,QTextFormat, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient
from PyQt5.QtWidgets import QSystemTrayIcon,QShortcut,QPlainTextEdit,QMenu,QAction, QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QTextEdit, QSplitter, QGraphicsDropShadowEffect
from PyQt5.QtCore import QCoreApplication,QRegExp, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent
from main import Ui_MainWindow
from PyQt5.Qsci import *
from subprocess import call
import sys
import os
import platform
import syntax
import json
import re
GLOBAL_STATE = 0
class SideGrip(QtWidgets.QWidget):
    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)
        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.add = editor


    def sizeHint(self):
        return Qsize(self.add.editor.lineNumberAreaWidth(), 1)


    def paintEvent(self, event):
        self.add.lineNumberAreaPaintEvent(event)
class theme_():
    with open('data.json') as f:
         data = json.load(f)
    background = data['background']
    textColor = data['text-color']
class uimain(QMainWindow):
    _gripSize = 2
    def numbers_to_strings(argument):
        switcher = {
            0: "red",
            1: "blue",
            2: "grean",
        }

        # get() method of dictionary data type returns
        # value of passed argument if it is present
        # in dictionary otherwise second argument will
        # be assigned as default value of passed argument
        return switcher.get(argument, "nothing")
    def __init__(self):
        themes = theme_()
        print(themes.background)

        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Adding options to the System Tray

        if themes.background == "white":
            self.ui.centralwidget.setStyleSheet("background-color:#fff; border-radius:5px;")
            self.ui.menubar.setStyleSheet("QMenuBar{\n"
        "top: 20px;\n"
        "color: black;\n"
        "background-color:#fff;\n"
        "font-size: 13px;\n"
        "font-family: arial;\n"
        "border-top: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
        "}\n"
        "QMenuBar::icon{\n"
        "    width: 20px;\n"
        "    height: 20px;\n"
        "}\n"
        "QMenuBar::item {\n"
        " right: 20px;\n"
        "left: 10px;\n"
        "margin-right: 14px;\n"
        "margin-top : 24.2px;\n"
        " }\n"
        "QMenuBar::item:pressed {\n"
        "    background-color: #fff;\n"
        "border-bottom: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
        "}\n"
        "QMenuBar::item:selected  {\n"
        "    height: 30px;\n"
        "    background-color: #fff;\n"
        "border-bottom: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
        "}")
            self.ui.pushButton.setStyleSheet("QPushButton{\n"
        " background-color:#fff;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " background: #fff;\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
            self.ui.pushButton_2.setStyleSheet("QPushButton{\n"
        " background-color:#fff;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " background: white;\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
            self.ui.pushButton_3.setStyleSheet("QPushButton{\n"
        " background-color:#fff;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " background: white;\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
            self.ui.pushButton_4.setStyleSheet("QPushButton{\n"
        " background-color:#fff;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " background: #fff;\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")


        if themes.background == "black":
            self.ui.centralwidget.setStyleSheet("background-color:black;")
            self.ui.menubar.setStyleSheet("QMenuBar{\n"
        "top: 20px;\n"
        "color: rgb(255, 255, 255);\n"
        "background-color:black;\n"
        "font-size: 13px;\n"
        "font-family: arial;\n"
        "border-top: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
        "}\n"
        "QMenuBar::icon{\n"
        "    width: 20px;\n"
        "    height: 20px;\n"
        "}\n"
        "QMenuBar::item {\n"
        " right: 20px;\n"
        "left: 10px;\n"
        "margin-right: 14px;\n"
        "margin-top : 24.2px;\n"
        " }\n"
        "QMenuBar::item:pressed {\n"
        "    background-color: black;\n"
        "border-bottom: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
        "}\n"
        "QMenuBar::item:selected  {\n"
        "    height: 30px;\n"
        "    background-color: black;\n"
        "border-bottom: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));\n"
        "}")
            self.ui.pushButton.setStyleSheet("QPushButton{\n"
        "background-color:black;\n"
        "border-style: none;\n"
        "}\n")
            self.ui.pushButton.setStyleSheet("QPushButton{\n"
        " background-color:black;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
            self.ui.pushButton_2.setStyleSheet("QPushButton{\n"
        " background-color:black;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
            self.ui.pushButton_3.setStyleSheet("QPushButton{\n"
        " background-color:black;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
            self.ui.pushButton_4.setStyleSheet("QPushButton{\n"
        " background-color:black;\n"
        "border-style: none;\n"
        "}\n"
        "QPushButton:hover{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}\n"
        "QPushButton:selected{\n"
        " border-left: 3px solid  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(3, 167, 255, 255), stop:1 rgba(199, 255, 248, 255));;\n"
        "}")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setStyleSheet("""border-radius: 5px; 
                            background: rgb(22, 24, 33);""")
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge), 
            SideGrip(self, QtCore.Qt.TopEdge), 
            SideGrip(self, QtCore.Qt.RightEdge), 
            SideGrip(self, QtCore.Qt.BottomEdge), 
        ]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]
        self.horizontalLayout_9 = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.ui.actionAdd_Tab.triggered.connect(self.add)
        self.ui.actionSave_as_Ctrl_S.triggered.connect(self.file_saveas)
        self.ui.actionSave_Ctrl_S.triggered.connect(self.file_save)
        self.ui.statusbar.showMessage("Pycos Visual | ConrED Studio")
        self.ui.tabWidget.currentIndex()
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.pushButton_6.clicked.connect(self.close)
        self.ui.pushButton_7.clicked.connect(self.showMinimized)
        self.ui.pushButton_5.clicked.connect(self.maximize_restore)
        self.ui.actionOpen_File_Ctrl_N.triggered.connect(self.add)
        self.ui.actionEdit.triggered.connect(self.theme)
        self.ui.actionOpen_Folder_Ctrl_Alt_N.triggered.connect(self.folder)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_18)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_19)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_20)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_21)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_27)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_28)
        self.ui.statusbar.addPermanentWidget(self.ui.pushButton_29)
        self.ui.pushButton_22.clicked.connect(lambda: self.toggleMenu(200, True))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.tabWidget_2.setTabText(self.ui.tabWidget_2.indexOf(self.ui.tab_3), "Search"))
        self.ui.pushButton.clicked.connect(self.home)
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_6))
        self.ui.pushButton_23.clicked.connect(self.store)
        self.ui.pushButton_24.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_4))
        self.ui.actionColor.triggered.connect(self.colorr)
        self.ui.actionNew_Window.triggered.connect(self.New)
        self.open_new_file_shortcut = QShortcut(QKeySequence('Ctrl+O'), self)
        self.open_new_file_shortcut.activated.connect(self.add)
        self.open_save_file_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.open_save_file_shortcut.activated.connect(self.file_save)
        self.open_sav_file_shortcut = QShortcut(QKeySequence('Ctrl+Shift+S'), self)
        self.open_sav_file_shortcut.activated.connect(self.file_saveas)
        self.ui.horizontalLayout_2.addWidget(self.ui.menubar)
        self.ui.horizontalLayout_15.addWidget(self.ui.statusbar)
        self.ui.menubar.children()[0].setIcon(QtGui.QIcon('menuover.png'))
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        self.anim2 = QPropertyAnimation(self.ui.label_2, b"geometry")
        self.anim2.setDuration(1700)
        self.anim2.setStartValue(QRect(133,75, 200,200))
        self.anim2.setEndValue(QRect(133, 50, 200,200))
        self.anim2.start()
        self.ui.horizontalLayout_2.addWidget(self.ui.frame_6)
        self.path = None
        self.ui.centralwidget.setStyleSheet("""border-radius: 5px;""")
        self.ui.horizontalLayout_2.addWidget(self.ui.frame_3)
        shadow6 = QGraphicsDropShadowEffect()
        shadow6.setXOffset(10)
        shadow6.setYOffset(0)
        shadow6.setBlurRadius(15)
        self.ui.centralwidget.setGraphicsEffect(shadow6)
        self.ui.tab_2.setGraphicsEffect(shadow6)
        if self.resize(848, 576):
            self.ui.verticalLayout_14 = QtWidgets.QHBoxLayout(self.ui.page_7)
            self.ui.verticalLayout_14.addWidget(self.ui.comboBox_2)
            self.ui.verticalLayout_14.addWidget(self.ui.comboBox)
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, self.maximize_restore)

        def moveWindow(event):
            # RESTORE BEFORE MOVE
            if uimain.returnStatus() == 1:
                self.maximize_restore()
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

                # SET TITLE BAR
        self.ui.frame_6.mouseMoveEvent = moveWindow
        self.ui.frame_6.mouseDoubleClickEvent = dobleClickMaximizeRestore
    def home(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_3)
        self.ui.tabWidget_2.setTabText(self.ui.tabWidget_2.indexOf(self.ui.tab_3), "Project")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE

        # IF NOT MAXIMIZED
        if status == 0:
            self.showMaximized()

            # SET GLOBAL TO 1
            GLOBAL_STATE = 1

            # IF MAXIMIZED REMOVE MARGINS AND BORDER RADIUS
            self.ui.pushButton_5.setToolTip("Restore")
            self.ui.pushButton_5.setIcon(QtGui.QIcon(u"restore_icon.svg"))
            self.ui.centralwidget.setStyleSheet("""QWidget{
    background-color:rgb(22, 24, 33);
}
                """)
            self._gripSize = False
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.ui.pushButton_5.setToolTip("Maximize")
            self.ui.pushButton_5.setIcon(QtGui.QIcon(u"maximize_icon.svg"))
            self.ui.centralwidget.setStyleSheet("""QWidget{
    background-color:rgb(22, 24, 33);
    border-radius: 5px;
}
                """)
            self._gripSize = True
    def store(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_5)
        self.ui.tabWidget_2.setTabText(self.ui.tabWidget_2.indexOf(self.ui.tab_3), "Store")
    def returnStatus():
        return GLOBAL_STATE


    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    def toggleMenu(self, maxWidth, enable):
        if enable:
            # GET WIDTH
            width = self.ui.frame.width()
            maxExtend = maxWidth
            standard = 51

            # SET MAX WIDTH
            if width == 51:
                widthExtended = maxExtend
                self.ui.pushButton_22.setText("Menu")
                self.ui.pushButton.setText("Explore")
                self.ui.pushButton_2.setText("Search")
                self.ui.pushButton_3.setText("Run")
                self.ui.pushButton_4.setText("Account")
                self.ui.pushButton_24.setText("Settings")
                self.ui.pushButton_23.setText("Library")
            else:
                widthExtended = standard
                self.ui.pushButton_22.setText("")
                self.ui.pushButton.setText("")
                self.ui.pushButton_2.setText("")
                self.ui.pushButton_3.setText("")
                self.ui.pushButton_4.setText("")
                self.ui.pushButton_24.setText("")
                self.ui.pushButton_23.setText("")

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    def colorr(self):
        self.plainTextEdit.setPaper(QColor("#30786e"))
    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), 
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), 
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()
    def New(self):
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setStyleSheet("background-color: #1f2e38;")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)

        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.__myFont = QFont('consolas')
        self.__myFont.setPointSize(14)
        self.plainTextEdit = QsciScintilla(self.tab_4)
        self.lineNumberArea = LineNumberArea(self)
        fontmetrics = QFontMetrics(self.__myFont)
        self.plainTextEdit.setIndentationsUseTabs(False)
        self.plainTextEdit.setIndentationWidth(4)
        self.plainTextEdit.setIndentationGuidesBackgroundColor(QColor("#b1c5e3"))
        self.plainTextEdit.setCaretWidth(1)
        self.plainTextEdit.setBackspaceUnindents(True)


        self.plainTextEdit.setIndentationGuides(True)
        self.plainTextEdit.setColor(QColor("#b1c5e3"))
        self.plainTextEdit.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
        # Multiple cursor support
        self.plainTextEdit.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
        self.plainTextEdit.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
        self.plainTextEdit.SendScintilla(
            QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)
        self.plainTextEdit.setMarginWidth(0, fontmetrics.width("00000") + 5)
        self.plainTextEdit.setFolding(QsciScintilla.PlainFoldStyle)
        self.__lexer = MyLexer(self.plainTextEdit)
        self.plainTextEdit.setLexer(self.__lexer)
        self.plainTextEdit.setCaretLineBackgroundColor(QColor("#282a3a"))
        self.plainTextEdit.setCaretLineVisible(True)
        self.plainTextEdit.setMarginsForegroundColor(QColor("#b1c5e3"))

        self.plainTextEdit.setStyleSheet(
        "QsciScintilla{\n"
        "   background-color: rgb(38, 56, 70);\n"
        "   border-style: none;\n"
        "   font-family: consolas;\n"
        "   color: #b1c5e3;\n"
        "   font-size: 16px;\n"
        "   selection-background-color: rgb(74, 109, 135, .2)\n"
        "}\n"
        "QScrollBar::sub-page{\n"
        "background: none;\n"
        "}\n"
        "\n"
        "QScrollBar::add-page:vertical {\n"
        "background:none;\n"
        "}\n"
        "QScrollBar:vertical {\n"
        "   border: 0px solid #999999;\n"
        "   background: rgb(0, 13, 26,0.4);\n"
        "   width:30px;    \n"
        "   margin: 0px 0px 0px 0px;\n"
        "   border-radius: 4px;\n"
        "}\n"
        "   QScrollBar::handle:vertical {         \n"
        "   \n"
        "       min-height: 0px;\n"
        "       border: 0px solid red;\n"
        "       border-radius: 2px;\n"
        "   \n"
        "       background-color:#76909c;\n"
        "   }\n"
        "   QScrollBar::add-line:vertical {       \n"
        "       height: 0px;\n"
        "       subcontrol-position: bottom;\n"
        "       subcontrol-origin: margin;\n"
        "        }\n"
        "        QScrollBar::sub-line:vertical {\n"
        "            height: 0 px;\n"
        "            subcontrol-position: top;\n"
        "            subcontrol-origin: margin;\n"
        "        }\n"
        "QScrollBar:horizontal {\n"
        "   border: 0px solid #999999;\n"
        "   background: rgb(0, 13, 26);\n"
        "   height:10px;    \n"
        "   margin: 0px 0px 0px 0px;\n"
        "   border-radius: 2px;\n"
        "}\n"
        "   QScrollBar::handle:horizontal {         \n"
        "\n"
        "       height: 10px;\n"
        "       min-height: 0px;\n"
        "       border: 0px solid red;\n"
        "       border-radius: 4px;\n"
        "\n"
        "       background-color: #76909c;\n"
        "   }\n"
        "   QScrollBar::handle:hover {         \n"
        "\n"
        "       border-radius: 0px;\n"
        "\n"
        "       background-color: #76909c;\n"
        "   }\n"
        "   QScrollBar::add-line:horizontal {       \n"
        "       height: 0px;\n"
        "       subcontrol-position: bottom;\n"
        "       subcontrol-origin: margin;\n"
        "        }\n"
        "        QScrollBar::sub-line:horizontal {\n"
        "            height: 0 px;\n"
        "            subcontrol-position: top;\n"
        "            subcontrol-origin: margin;\n"
        "        }\n"
        "")
        extraSelections = []
        StandardBackground = [36, 53, 66]
        def color_to_sc(c):
            return (c[0] & 0xFF) | ((c[1] & 0xFF) << 8) | ((c[2] & 0xFF) << 16)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setCaretForegroundColor(QColor('rgb(38, 56, 70)'))
        self.plainTextEdit.setFont(self.__myFont)
        self.plainTextEdit.setWrapMode(QsciScintilla.WrapWord)
        self.plainTextEdit.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.plainTextEdit.setWrapIndentMode(QsciScintilla.WrapIndentIndented)
        self.plainTextEdit.setSelectionBackgroundColor(QColor("#415c72"))
        self.plainTextEdit.resetSelectionForegroundColor()

        # 2. End-of-line mode
        # --------------------
        self.plainTextEdit.setEolMode(QsciScintilla.EolWindows)
        self.plainTextEdit.setEolVisibility(False)
        self.plainTextEdit.SendScintilla(self.plainTextEdit.SCI_STYLESETBACK, self.plainTextEdit.STYLE_LINENUMBER, color_to_sc(StandardBackground))
        self.plainTextEdit.SendScintilla(self.plainTextEdit.SCI_SETFOLDMARGINHICOLOUR, True, color_to_sc(StandardBackground))
        self.plainTextEdit.SendScintilla(self.plainTextEdit.SCI_SETFOLDMARGINCOLOUR, True, color_to_sc(StandardBackground))
        self.plainTextEdit.setCaretForegroundColor(QColor("#21d3ff"))
        self.plainTextEdit.setMarginsBackgroundColor(QColor("#273947"))
        self.__lexer.setPaper(QColor('#273947'))
        self.horizontalLayout_5.addWidget(self.plainTextEdit)
        self.ui.tabWidget.addTab(self.tab_4, "Untitled")
    def add(self):
        for i in range(1):
            self.tab_3 = QtWidgets.QWidget()
            def moveWindow(event):
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

                    # SET TITLE BAR
            
            self.tab_3.setStyleSheet("background-color: rgb(22, 24, 33);")
            self.horizontalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
            self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_5.setSpacing(0)
            shadow5 = QGraphicsDropShadowEffect()
            shadow5.setXOffset(0)
            shadow5.setYOffset(0)
            shadow5.setBlurRadius(60)
            self.ui.menubar.setGraphicsEffect(shadow5)
            self.frame_8 = QtWidgets.QFrame(self.tab_3)
            self.frame_8.setGraphicsEffect(shadow5)
            
            self.frame_8.setMinimumSize(QtCore.QSize(1, 27))
            self.frame_8.setMaximumSize(QtCore.QSize(16777215, 27))
            self.frame_8.setStyleSheet("border-bottom: 1px solid rgb(19, 28, 35,.3);\n "
                "background-color: #282a3a;")
            self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_8.setObjectName("frame_8")
            self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_8)
            self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_13.setSpacing(0)
            self.horizontalLayout_13.setObjectName("horizontalLayout_13")
            self.pushButton_31 = QtWidgets.QPushButton(self.frame_8)
            self.pushButton_31.setMinimumSize(QtCore.QSize(60, 0))
            self.pushButton_31.setMaximumSize(QtCore.QSize(60, 35))
            self.pushButton_31.setStyleSheet("QPushButton{\n"
    "    border-style: none;\n"
    "    background-color: #282a3a;\n"
    "    color: rgb(93, 178, 197);\n"
    "}\n"
    "QPushButton:hover{\n"
    "    border-style: none;\n"
    "    \n"
    "    background-color: rgb(33, 49, 60);\n"
    "    color: rgb(42, 91, 93);\n"
    "}")
            self.pushButton_31.setObjectName("pushButton_31")
            self.horizontalLayout_13.addWidget(self.pushButton_31)
            self.pushButton_30 = QtWidgets.QPushButton(self.frame_8)
            self.pushButton_30.setMinimumSize(QtCore.QSize(40, 0))
            self.pushButton_30.setMaximumSize(QtCore.QSize(16777215, 25))
            self.pushButton_30.setStyleSheet("QPushButton{\n"
    "    border-style: none;\n"
    "    background-color: #282a3a;\n"
    "    color: rgb(93, 178, 197);\n"
    "}\n"
    "QPushButton:hover{\n"
    "    border-style: none;\n"
    "    \n"
    "    background-color: rgb(33, 49, 60);\n"
    "    color: rgb(42, 91, 93);\n"
    "}")
            self.pushButton_30.setObjectName("pushButton_30")
            self.horizontalLayout_13.addWidget(self.pushButton_30)

            spacerItem1 = QtWidgets.QSpacerItem(26, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout_13.addItem(spacerItem1)
            self.horizontalLayout_5.addWidget(self.frame_8)
            self.horizontalLayout_5.setObjectName("horizontalLayout_5")
            self.__myFont = QFont('consolas')
            self.__myFont.setPointSize(14)
            self.plainTextEdit = QsciScintilla(self.tab_3)
            self.lineNumberArea = LineNumberArea(self)
            fontmetrics = QFontMetrics(self.__myFont)
            self.plainTextEdit.setIndentationsUseTabs(False)
            self.plainTextEdit.setIndentationWidth(4)
            self.plainTextEdit.setIndentationGuidesBackgroundColor(QColor("#2c2f3f"))
            self.plainTextEdit.setCaretWidth(1)
            self.plainTextEdit.setBackspaceUnindents(True)
            


            self.plainTextEdit.setIndentationGuides(True)
            self.plainTextEdit.setColor(QColor("#b1c5e3"))
            self.plainTextEdit.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
            # Multiple cursor support
            self.plainTextEdit.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
            self.plainTextEdit.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
            self.plainTextEdit.SendScintilla(
                QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)
            self.plainTextEdit.setMarginWidth(0, fontmetrics.width("00000") + 5)
            self.plainTextEdit.setFolding(QsciScintilla.BoxedFoldStyle)
            self.font = QFont()  
            self.font.setFamily("consolas")  
            self.font.setPointSize(14)  
            self.font.setFixedPitch(True)  
            
            self.plainTextEdit.setFont(self.font)
            
            
            ## Add autocompletion strings
            
            self.plainTextEdit.setCaretLineBackgroundColor(QColor("#1e1f2b"))
            self.plainTextEdit.setCaretLineVisible(True)
            self.plainTextEdit.setMarginsForegroundColor(QColor("#55a5a6"))
            self.plainTextEdit.setAutoCompletionThreshold(1)
            ## Tell the editor we are using a QsciAPI for the autocompletion
            self.plainTextEdit.setAutoCompletionSource(QsciScintilla.AcsAPIs)

            self.plainTextEdit.setStyleSheet(
            "QsciScintilla{\n"
            "   background-color: rgb(38, 56, 70);\n"
            "   border-style: none;\n"
            "   font-family: consolas;\n"
            "   color: #b1c5e3;\n"
            "   font-size: 16px;\n"
            "   selection-background-color: rgb(74, 109, 135, .2)\n"
            "}\n"
            "QScrollBar::sub-page{\n"
            "background: none;\n"
            "}\n"
            "\n"
            "QScrollBar::add-page:vertical {\n"
            "background:none;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "   border: 0px solid #999999;\n"
            "   background: #273947;\n"
            "   width:12px;    \n"
            "   margin: 0px 0px 0px 0px;\n"
            "   border-radius: 0px;\n"
            "}\n"
            "   QScrollBar::handle:vertical {         \n"
            "   \n"
            "       min-height: 0px;\n"
            "       border: 0px solid red;\n"
            "       border-radius: 2px;\n"
            "   \n"
            "       background-color:rgb(118, 144, 156,.2);\n"
            "       min-height: 15px;"
            "   }\n"
            "   QScrollBar::add-line:vertical {       \n"
            "       height: 0px;\n"
            "       subcontrol-position: bottom;\n"
            "       subcontrol-origin: margin;\n"
            "        }\n"
            "        QScrollBar::sub-line:vertical {\n"
            "            height: 0 px;\n"
            "            subcontrol-position: top;\n"
            "            subcontrol-origin: margin;\n"
            "        }\n"
            "QScrollBar:horizontal {\n"
            "   border: 0px solid #999999;\n"
            "   background: rgb(0, 13, 26);\n"
            "   height:4px;    \n"
            "   margin: 0px 0px 0px 0px;\n"
            "   border-radius: 2px;\n"
            "}\n"
            "   QScrollBar::handle:horizontal {         \n"
            "\n"
            "       height: 6px;\n"
            "       min-height: 0px;\n"
            "       border: 0px solid red;\n"
            "       border-radius: 4px;\n"
            "\n"
            "       background-color: #76909c;\n"
            "   }\n"
    		"   QScrollBar::handle:hover {         \n"
            "\n"
    		"		border-radius: 0px;\n"
            "\n"
            "       background-color: rgb(118, 144, 156,.5);\n"
            "   }\n"
            "   QScrollBar::add-line:horizontal {       \n"
            "       height: 0px;\n"
            "       subcontrol-position: bottom;\n"
            "       subcontrol-origin: margin;\n"
            "        }\n"
            "        QScrollBar::sub-line:horizontal {\n"
            "            height: 0 px;\n"
            "            subcontrol-position: top;\n"
            "            subcontrol-origin: margin;\n"
            "        }\n"
            "")
            extraSelections = []
            StandardBackground = [36, 53, 66]
            def color_to_sc(c):
                return (c[0] & 0xFF) | ((c[1] & 0xFF) << 8) | ((c[2] & 0xFF) << 16)
            self.plainTextEdit.setObjectName("plainTextEdit")
            self.plainTextEdit.setCaretForegroundColor(QColor('rgb(38, 56, 70)'))
            self.plainTextEdit.setFont(self.__myFont)
            self.plainTextEdit.setWrapIndentMode(QsciScintilla.WrapIndentIndented)
            self.plainTextEdit.setSelectionBackgroundColor(QColor("#415c72"))
            self.plainTextEdit.resetSelectionForegroundColor()
            

            # 2. End-of-line mode
            # --------------------
            self.plainTextEdit.setEolMode(QsciScintilla.EolWindows)
            self.plainTextEdit.setEolVisibility(False)
            self.plainTextEdit.SendScintilla(self.plainTextEdit.SCI_STYLESETBACK, self.plainTextEdit.STYLE_LINENUMBER, color_to_sc(StandardBackground))
            self.plainTextEdit.SendScintilla(self.plainTextEdit.SCI_SETFOLDMARGINHICOLOUR, True, color_to_sc(StandardBackground))
            self.plainTextEdit.SendScintilla(self.plainTextEdit.SCI_SETFOLDMARGINCOLOUR, True, color_to_sc(StandardBackground))
            self.plainTextEdit.setCaretForegroundColor(QColor("#21d3ff"))
            self.plainTextEdit.setMarginsBackgroundColor(QColor("#1e1f2b"))
            
            self.horizontalLayout_5.addWidget(self.plainTextEdit)
            self.plainTextEdit.setEdgeMode(QsciScintilla.EdgeLine)  
            self.plainTextEdit.setEdgeColumn(60)  
            self.plainTextEdit.setEdgeColor(QColor("#1e1f2b"))
            
            qfd = QFileDialog()
            path = "D:\ennine\SIG HTB\BGN"
            filter = "*.py"
            cpp = "*.cpp"

            filename = QtWidgets.QFileDialog.getOpenFileName(self,path, filter, cpp)
            url = QUrl.fromLocalFile(filename[0])

            print(str(format(url.fileName())))
            print(url.fileName().split(".")[1])
            def lineNumberAreaPaintEvent(self, event):
                mypainter = QPainter(self.lineNumberArea)

                mypainter.fillRect(event.rect(), QColor('#fff').lighter(40))

                block = self.plainTextEdit.firstVisibleBlock()
                blockNumber = block.blockNumber()
                top = self.plainTextEdit.blockBoundingGeometry(block).translated(self.plainTextEdit.contentOffset()).top()
                bottom = top + self.plainTextEdit.blockBoundingRect(block).height()

                # Just to make sure I use the right font
                height = self.plainTextEdit.fontMetrics().height()
                while block.isValid() and (top <= event.rect().bottom()):
                    if block.isVisible() and (bottom >= event.rect().top()):
                        number = str(blockNumber + 1)
                        mypainter.setPen(QColor('#fff'))
                        mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                         Qt.AlignRight, number)
                    block = block.next()
                    top = bottom
                    bottom = top + self.plainTextEdit.blockBoundingRect(block).height()
                    blockNumber += 1
            def resizeEvent(self, event):
                super().resizeEvent(event)
                cr = self.plainTextEdit.contentsRect()
                self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))
            self.ui.tabWidget.addTab(self.tab_3, "" + str(format(url.fileName())))
            self.ui.tabWidget.mouseMoveEvent = moveWindow
            
            if url.fileName().split(".")[1] == "cpp":
                print("123")
                self.ui.pushButton_18.setText("C++   ")
                self.pushButton_31.setText("C++")
                self.pushButton_30.setText("utf-8")

            if url.fileName().split(".")[1] == "h":

                print("123")

                self.ui.pushButton_18.setText("C++   ")

                self.pushButton_31.setText("C++")

                self.pushButton_30.setText("utf-8")

            if url.fileName().split(".")[1] == "js":

                print("123")

                self.ui.pushButton_18.setText("C++   ")

                self.pushButton_31.setText("Javascript")

                self.pushButton_30.setText("utf-8")
                self.lexer = QsciLexerJavaScript()
                self.lexer.setFont(self.font)
                self.plainTextEdit.setLexer(self.lexer)
                self.lexer.setColor(QColor("#b1c5e3"), QsciLexerJavaScript.Default)  
                self.lexer.setPaper(QColor("#ffffff"))

            if url.fileName().split(".")[1] == "html":

                print("123")

                self.ui.pushButton_18.setText("C++   ")

                self.pushButton_31.setText("HTML")

                self.pushButton_30.setText("utf-8")
                self.lexer = QsciLexerHTML()
                self.lexer.setFont(self.font)  
                self.plainTextEdit.setLexer(self.lexer)
                self.lexer.setColor(QColor("#b1c5e3"), QsciLexerHTML.Default)  
                self.lexer.setPaper(QColor("#282a3a"))
                self.lexer.setColor(QColor("#71ad81"),QsciLexerHTML.HTMLNumber)
                self.lexer.setColor(QColor("#71ad81"),QsciLexerHTML.OtherInTag )

                self.lexer.setColor(QColor("#b59c4a"),QsciLexerHTML.Tag )
                self.lexer.setColor(QColor("#b59c4a"),QsciLexerHTML.Attribute  )
                self.lexer.setColor(QColor("#b59c4a"),QsciLexerHTML.HTMLDoubleQuotedString)
                self.lexer.setColor(QColor("#b59c4a"),QsciLexerHTML.HTMLSingleQuotedString )
            _translate = QtCore.QCoreApplication.translate
            if filename[0]: 
                # try opening path 
                try: 
                    with open(filename[0], 'rU') as f: 
                        # read the file 
                        text = f.read() 

      
                # if some error occured 
                except Exception as e: 
      
                    # show error using critical method 
                    self.dialog_critical(str(e)) 
                # else 
                else: 
                    # update path value 
                    for z in range(1):
                        self.path = filename[0]
                        break
                    

      
                    # update the text 
                    self.plainTextEdit.setText(text) 
                if url.fileName().split(".")[1] == "py":
                    print("xyz")
                    for i in range(1):
                        self.path1= filename[0]
                        self.pushButton_32 = QtWidgets.QPushButton(self.frame_8)
                        self.pushButton_32.setMinimumSize(QtCore.QSize(60, 0))
                        self.pushButton_32.setMaximumSize(QtCore.QSize(60, 35))
                        self.pushButton_32.setText("Run")
                        self.pushButton_32.clicked.connect(lambda: call(["python", self.path1]))
                        self.pushButton_32.setStyleSheet("QPushButton{\n"
                "    border-style: none;\n"
                "    background-color: #282a3a;\n"
                "    color: rgb(93, 178, 197);\n"
                "}\n"
                "QPushButton:hover{\n"
                "    border-style: none;\n"
                "    \n"
                "    background-color: rgb(33, 49, 60);\n"
                "    color: rgb(42, 91, 93);\n"
                "}")
                        self.pushButton_32.setObjectName("pushButton_31")
                        break

                    self.horizontalLayout_13.addWidget(self.pushButton_32)
                    self.ui.pushButton_18.setText("Python   ")
                    self.pushButton_31.setText("Python")
                    self.pushButton_30.setText("utf-8")
                    self.lexer = QsciLexerPython()
                    self.lexer.setFont(self.font)  
                      
                    #high light code  
                    self.lexer.setColor(QColor("#b1c5e3"))  
                    self.lexer.setPaper(QColor("#333333"))  
                    self.lexer.setColor(QColor("#5BA5F7"),QsciLexerPython.ClassName)  
                    self.lexer.setColor(QColor("#ff7577"),QsciLexerPython.Keyword)  
                    self.lexer.setColor(QColor("#00FF40"),QsciLexerPython.Comment)  
                    self.lexer.setColor(QColor("#BD4FE8"),QsciLexerPython.Number)  
                    self.lexer.setColor(QColor("#faf36b"),QsciLexerPython.DoubleQuotedString)  
                    self.lexer.setColor(QColor("#faf36b"),QsciLexerPython.TripleSingleQuotedString)  
                    self.lexer.setColor(QColor("#faf36b"),QsciLexerPython.TripleDoubleQuotedString)  
                    self.lexer.setColor(QColor("#faf36b"),QsciLexerPython.DoubleQuotedString)  
                    self.lexer.setColor(QColor("#04F452"),QsciLexerPython.FunctionMethodName)  
                    self.lexer.setColor(QColor("#b1c5e3"),QsciLexerPython.Operator)  
                    self.lexer.setColor(QColor("#b1c5e3"),QsciLexerPython.Identifier)  
                    self.lexer.setColor(QColor("#F1E607"),QsciLexerPython.CommentBlock)  
                    self.lexer.setColor(QColor("#F1E607"),QsciLexerPython.UnclosedString)  
                    self.lexer.setColor(QColor("#F1E607"),QsciLexerPython.HighlightedIdentifier)  
                    self.lexer.setColor(QColor("#F1E607"),QsciLexerPython.Decorator) 
                    api = QsciAPIs(self.lexer) 
                    api.add("if")
                    api.add("while")
                    api.add("for")
                    api.add("imput")
                    api.add("def")
                    api.add("__init__")
                    api.add("class")
                    api.add("False")
                    api.add("True")
                    api.add("self")
                    api.add("__name__")
                    api.add("len")
                    api.add("tuple")
                    api.add("else")
                    api.add("elif")
                    api.add("pass")
                    api.add("void")
                    api.add("int")
                    api.add("include")
                    api.add("import")
                    api.add("from")
                    api.add("local")
                    api.add("printf")
                    api.add("Public")
                    api.add("Private")
                    api.add("<div>")
                    api.add("</div>")
                    api.add("<body>")
                    api.add("</body>")
                    api.add("<!DOCTYPE html>")
                    api.add("<abbr>")
                    api.add("</abbr>")
                    api.add("<a>")
                    api.add("</a>")
                    api.add("<b>")
                    api.add("</b>")
                    api.add("<p>")
                    api.add("</p>")
                    api.add("<header>")
                    api.add("</header>")
                    api.add("<link>")
                    api.add("class=""")
                    api.add("href=""")
                    api.add("func")
                    api.add("<script")
                    api.add("<section>")
                    api.add("</section>")
                    api.add("<meta")
                    api.add("<nav>")
                    api.add("</nav>")
                    api.add("<option>")
                    api.add("</option>")
                    api.add("<img>")
                    api.add("<img src="" alt="">")
                    api.add("<param>")
                    api.add("<progress>")
                    api.add("</progress>")
                    api.add("<q>")
                    api.add("</q>")
                    api.add("<ul>")
                    api.add("</ul>")
                    api.add("<li>")
                    api.add("</li>")
                    api.add("<ruby>")
                    api.add("</ruby>")
                    api.add("</ruby>")
                    api.add("<select>")
                    api.add("</select>")
                    api.add("<span>")
                    api.add("</span>")
                    api.add("<time>")
                    api.add("</time>")
                    api.add("<u>")
                    api.add("</u>")
                    ## Compile the api for use in the lexer
                    api.prepare()
                    self.plainTextEdit.setLexer(self.lexer)
                    self.lexer.setPaper(QColor('#282a3a'))
            break

    def mousePressEvent(self, event):
            self.dragPos = event.globalPos()
    def close_tab(self,index):
          self.ui.tabWidget.removeTab(index)
    def theme(self):
        from Maintheme import ui_Uimain
        ui_Uimain()
        self.close()
    def text(self):
        STYLE = {
            'import' : QColor(Qt.red)
        }
        pass

    

    def folder(self):
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:')

    def file_save(self): 
  
        # if there is no save path 
        if self.path is None: 
  
            # call save as method 
            return self.file_saveas() 
  
        # else call save to path method
        self._save_to_path(self.path)
        self.ui.statusbar.showMessage("     Saved     ")
  
    # action called by save as action 
    def file_saveas(self): 
  
        # opening path 
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",  
                             "Python File (*.py);All files (*.*)") 
  
        # if dialog is cancelled i.e no path is selected 
        if not path: 
            # return this method 
            # i.e no action performed 
            return
  
        # else call save to path method 
        self._save_to_path(path)
        self.ui.statusbar.showMessage("     Saved     ")
    def _save_to_path(self, path): 
  
        # get the text 
        text = self.plainTextEdit.text() 
  
        # try catch block 
        try: 
  
            # opening file to write 
            with open(path, 'w') as f: 
  
                # write text in the file 
                f.write(text) 
  
        # if error occurs 
        except Exception as e: 
  
            # show error using critical 
            self.dialog_critical(str(e)) 
  
        # else do this 
        else: 
            # change path 
            self.path = path
    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    ## ==> DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect
    ## ==> START SELECTION
    def selectStandardMenu(self, widget):
        pass

    ## ==> RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.frame.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(deselectMenu(w.styleSheet()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    icon = QIcon("python.png")

    # Adding item on the menu bar
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    # Creating the options
    menu = QMenu()
    menu.setStyleSheet("QMenu {\n"
    "   /* background-color: #0F7070;*/\n"
    "    background-color: rgb(36, 51, 65);\n"
    "    border-top: none;\n"
    "    border-left:none;\n"
    "    border-right:none;\n"
    "    border-radius: 3px;\n"
    "    border-bottom:4px solid  rgb(44,205,112);;\n"
    "    color:#fff;;\n"
    "}\n"
    "\n"
    "QMenu::item {\n"
    "    spacing: 3px; /* spacing between menu bar items */\n"
    "    padding: 10px 85px 10px 20px;\n"
    "    background: transparent;\n"
    "}\n"
    "/*Does not work*/\n"
    "QMenu::item:selected {\n"
    "    background-color: rgb(52,73,94);\n"
    "    border-top: none;\n"
    "    border-left:none;\n"
    "    border-bottom:none;\n"
    "    border-left:3px solid  rgb(44,205,112);;\n"
    "}")
    option1 = QAction("Geeks for Geeks")
    option2 = QAction("GFG")
    menu.addAction(option1)
    menu.addAction(option2)

    tray.setContextMenu(menu)
    # To quit the app
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    window = uimain()
    window.show()
    menu.aboutToShow.connect(window.show)
    argument=0
    print(uimain.numbers_to_strings(argument))
    sys.exit(app.exec_())
