import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())