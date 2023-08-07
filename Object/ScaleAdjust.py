from PyQt5.QtWidgets import QMainWindow
from Object.Exception import *

class ScalePlotAdjust(QMainWindow):
    def __init__(self,MainWindows) -> None:
        super().__init__(MainWindows)

        # Initialize Object
        self.MainWindows = MainWindows
        self.MainWindows.scaleX.valueChanged.connect(self.MainWindows.chartFT.addjust_Plort)
        self.MainWindows.scaleYP.valueChanged.connect(self.MainWindows.chartFT.addjust_Plort)
        self.MainWindows.scaleYN.valueChanged.connect(self.MainWindows.chartFT.addjust_Plort)

    # def __ScaleX(self):
    #     try:
    #         msgPrint('SCALE_X : {}'.format(self.MainWindows.scaleX.value()))

    #     except Exception as e:
    #         print(str(e))