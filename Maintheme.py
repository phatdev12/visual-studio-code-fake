# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from theme import Ui_theme
from uiWhite import *
from uimain import *
from loadre import *
import json

class ui_Uimain(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_theme()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.toolButton.clicked.connect(self.close)
        self.show()
        self.ui.pushButton_2.clicked.connect(self.white)
        self.ui.pushButton_3.clicked.connect(self.black)
        self.ui.pushButton_4.clicked.connect(self.none)
        def moveWindow(event):
                    # RESTORE BEFORE MOVE

                    # IF LEFT CLICK MOVE WINDOW
                    if event.buttons() == Qt.LeftButton:
                        self.move(self.pos() + event.globalPos() - self.dragPos)
                        self.dragPos = event.globalPos()
                        event.accept()

                # SET TITLE BAR
        self.ui.frame.mouseMoveEvent = moveWindow
    def mousePressEvent(self, event):
            self.dragPos = event.globalPos()

    def white(self):
        
        data_dict = {"background": "white",
        "text-color": "red"
        }

        with open('data.json', 'w') as json_file:
            json.dump(data_dict, json_file)
        self.load = loadmain()
        self.close()
    def black(self):
        data_dict = {"background": "black",
        "text-color": "red"
        }

        with open('data.json', 'w') as json_file:
                json.dump(data_dict, json_file)
        self.load = loadmain()
        self.close()
    def blue(self):
        pass
    def none(self):
        data_dict = {"background": "none",
        "text-color": "red"
        }

        with open('data.json', 'w') as json_file:
            json.dump(data_dict, json_file)
        self.load = loadmain()
        self.close()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ui_Uimain()
    sys.exit(app.exec_())
