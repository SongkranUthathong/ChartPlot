from PyQt5.QtWidgets import QMainWindow
from Object.Exception import *
import os
import json

class ScalePlotAdjust(QMainWindow):
    def __init__(self,MainWindows) -> None:
        super().__init__(MainWindows)

        # Initialize Object
        self.MainWindows = MainWindows
        self.MainWindows.scaleX.valueChanged.connect(self.MainWindows.chartFT.addjust_Plort)
        self.MainWindows.scaleYP.valueChanged.connect(self.MainWindows.chartFT.addjust_Plort)
        self.MainWindows.scaleYN.valueChanged.connect(self.MainWindows.chartFT.addjust_Plort)
        self.loadSetValue()

    def loadSetValue(self):
        try:
            _dir1 = os.getcwd() + '//scale.json'
            with open(_dir1) as f:
                file_contents = json.load(f)
            # msgPrint(str(file_contents['x_scale']))
            # print(self.scale)
            self.MainWindows.scaleX.setValue(file_contents['x_scale'])
            self.MainWindows.scaleYP.setValue(file_contents['yp_scale'])
            self.MainWindows.scaleYN.setValue(file_contents['yn_scale'])
            pass
        except Exception as e:
            msgPrint(str(e))
    
    def writeScaleValue(self):
        try:
            _dir1 = os.getcwd() + '//scale.json'

            with open(_dir1) as f:
                __scale = json.load(f)
                __scale['x_scale'] = self.MainWindows.scaleX.value()
                __scale['yp_scale'] = self.MainWindows.scaleYP.value()
                __scale['yn_scale'] = self.MainWindows.scaleYN.value()
                # config_json['ip'] = self.data_configuration
            with open(_dir1, 'w') as f:
                json.dump(__scale, f)
            
            # msgPrint(":floppy_disk:",'[bold magenta] Scale :','[bold blue]'+__scale)
            pass
        except Exception as e:
            msgPrint(str(e))

    # def __ScaleX(self):
    #     try:
    #         msgPrint('SCALE_X : {}'.format(self.MainWindows.scaleX.value()))

    #     except Exception as e:
    #         print(str(e))