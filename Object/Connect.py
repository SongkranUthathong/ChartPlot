from PyQt5.QtWidgets import QMainWindow
from Object.Exception import *




class URConnect(QMainWindow):
    def __init__(self,MainWindows) -> None:
        super().__init__(MainWindows)

        # Initialize Object
        self.MainWindows = MainWindows
        self.MainWindows.btn_start.clicked.connect(self.__Connect)
        

    def __Connect(self):
        try:
            # print('Hello')
            # rtde_r = rtde_receive.RTDEReceiveInterface("192.168.47.128")
            # actual_q = rtde_r.getActualQ()       
            # msgPrint(actual_q)
            self.MainWindows.chartFT.start_thred()

        except Exception as e:
            print(str(e))
