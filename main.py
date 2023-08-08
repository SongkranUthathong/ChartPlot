import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox

from Object.ChartObject import *
from Object.Connect import *
from Object.Exception import *
from Object.ScaleAdjust import*

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    # region --------------> [ Load UI Windows From ] <--------------
        _dir1 = os.getcwd() + '//GUI//main.ui'
        loadUi(_dir1, self)
    # endregion

    # region --------------> [ Instance Widget UI ] <--------------
        self.chartFT = ForceTorqeChart(self)
        self.scaleAdjust = ScalePlotAdjust(self)
        URConnect(self)
    # endregion

    # region --------------> [ Load UI Windows From ] <--------------
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.scaleAdjust.writeScaleValue()
        else:
            event.ignore()    
    # endregion

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())