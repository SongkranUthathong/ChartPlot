import time
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QWidget
from PyQt5.QtCore import QObject, Qt, QTimer,QThread, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from Object.Exception import *
from rtde_receive import RTDEReceiveInterface as RTDEReceive

MAX = 100
MS = 10
class CustomThread(QThread):

    signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(CustomThread, self).__init__(parent)
        # self.rtde_r = rtde_receive.RTDEReceiveInterface("192.168.47.128")
        self.rtde_r = RTDEReceive("192.168.1.123")
        self.count = 1
        self.FX = [0] * MAX
        self.FY = [0] * MAX
        self.FZ = [0] * MAX
        self.TX = [0] * MAX
        self.TY = [0] * MAX
        self.TZ = [0] * MAX
    def run(self):
        # This method will be executed in a separate thread
        while True:
            actual_q = self.rtde_r.getActualTCPForce()
            # actual_q = self.rtde_r.getFtRawWrench()
            # actual_q = self.rtde_r.getActualQ()
            r2d = [180/np.pi]*6
            # actual_q = [actual_q[i] * r2d[i] for i in range(len(actual_q))]
            for i in range(MAX):
                if i < MAX - 1:
                    self.FX[i] = self.FX[i+1]
                    self.FY[i] = self.FY[i+1]
                    self.FZ[i] = self.FZ[i+1]
                    self.TX[i] = self.TX[i+1]
                    self.TY[i] = self.TY[i+1]
                    self.TZ[i] = self.TZ[i+1]
                else:
                    self.FX[i] = actual_q[0]
                    self.FY[i] = actual_q[1]
                    self.FZ[i] = actual_q[2]
                    self.TX[i] = actual_q[3]
                    self.TY[i] = actual_q[4]
                    self.TZ[i] = actual_q[5]
                self.count +=1
            self.signal.emit([np.array(self.FX),np.array(self.FY),np.array(self.FZ),np.array(self.TX),np.array(self.TY),np.array(self.TZ)])
            time.sleep(1/MS)  # Simulate a time-consuming operation
            

class PlotProfile(QWidget):
    def __init__(self, parent=None):
        super(PlotProfile, self).__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.sampling_interval = 1 / MS
        self.time_in_sec = np.arange(MAX) * self.sampling_interval
        # print(len(self.time_in_sec))


class ForceTorqeChart(QMainWindow):
    def __init__(self,MainWindows):
        super().__init__()

        self.MainWindows = MainWindows

        # SET Force & Torque Chart
        self.animated_widget1 = PlotProfile(self)
        self.animated_widget2 = PlotProfile(self)
        self.animated_widget1.ax.set_xlabel("Time (s)")
        self.animated_widget1.ax.set_ylabel("N")
        self.animated_widget1.ax.set_title('FORCE')
        self.animated_widget2.ax.set_xlabel("Time (s)")
        self.animated_widget2.ax.set_ylabel("N*m")
        self.animated_widget2.ax.set_title('TORQUE')
        self.animated_widget1.ax.set_xlim(0,10)
        self.animated_widget2.ax.set_xlim(0,10)
        self.animated_widget1.ax.set_ylim(-1,1)
        self.animated_widget2.ax.set_ylim(-1,1)
        self.ChartFX = self.animated_widget1.ax.plot(0,0,c='r',label='FX')[0]
        self.ChartFY = self.animated_widget1.ax.plot(0,0,c='g',label='FY')[0]
        self.ChartFZ = self.animated_widget1.ax.plot(0,0,c='b',label='FZ')[0]

        self.ChartTX = self.animated_widget2.ax.plot(0,0,c='r',label='TX')[0]
        self.ChartTY = self.animated_widget2.ax.plot(0,0,c='g',label='TY')[0]
        self.ChartTZ = self.animated_widget2.ax.plot(0,0,c='b',label='TZ')[0]
        self.animated_widget1.ax.legend()
        self.animated_widget2.ax.legend()
        layout1 = QVBoxLayout()
        layout1.addWidget(self.animated_widget1.canvas)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.animated_widget2.canvas)




        # Set Lay out to Widget
        self.MainWindows.chart_Force.setLayout(layout1)
        self.MainWindows.chart_Torque.setLayout(layout2)


    def start_thred(self):
        try:
            # Create an instance of the custom thread
            self.thread = CustomThread()

            # Connect the custom signal from the thread to a slot in the main GUI thread
            self.thread.signal.connect(self.on_thread_signal)

            # Start the thread
            self.thread.start()
        except Exception as e:
            msgPrint(str(e))


    def on_thread_signal(self, FTSensor):
        try:
            self._NDF = FTSensor
            # Set Data for FX
            self.ChartFX.set_ydata(FTSensor[0])
            # self.ChartFX.set_xdata(self.animated_widget1.time_in_sec)
            self.ChartFX.set_xdata(np.linspace(0,10,MAX))
            # Set Data for FY
            self.ChartFY.set_ydata(FTSensor[1])
            # self.ChartFY.set_xdata(self.animated_widget1.time_in_sec)
            self.ChartFY.set_xdata(np.linspace(0,10,MAX))
            # # Set Data for FZ
            self.ChartFZ.set_ydata(FTSensor[2])
            # self.ChartFZ.set_xdata(self.animated_widget1.time_in_sec)
            self.ChartFZ.set_xdata(np.linspace(0,10,MAX))


            # # Set Data for TX
            # self.ChartTX.set_ydata(FTSensor[3])
            # # self.ChartTX.set_xdata(self.animated_widget2.time_in_sec)
            # self.ChartTX.set_xdata(np.linspace(0,10,MAX))
            # # Set Data for TY
            # self.ChartTY.set_ydata(FTSensor[4])
            # # self.ChartTY.set_xdata(self.animated_widget2.time_in_sec)
            # self.ChartTY.set_xdata(np.linspace(0,10,MAX))
            # # # Set Data for TZ
            # self.ChartTZ.set_ydata(FTSensor[5])
            # # self.ChartTZ.set_xdata(self.animated_widget2.time_in_sec)
            # self.ChartTZ.set_xdata(np.linspace(0,10,MAX))


            # UPDATE CHART
            self.animated_widget1.canvas.blit(self.animated_widget1.figure.bbox)
            self.animated_widget1.canvas.flush_events()
            self.animated_widget1.canvas.draw()

            # self.animated_widget2.canvas.blit(self.animated_widget2.figure.bbox)
            # self.animated_widget2.canvas.flush_events()
            # self.animated_widget2.canvas.draw()

            # msgPrint(self._NDF[0][MAX-1])
        except Exception as e:
            msgPrint(str(e))

    def addjust_Plort(self):
        try:
            
            scale_x = self.MainWindows.scaleX.value()
            scale_yp = self.MainWindows.scaleYP.value()
            scale_yn = self.MainWindows.scaleYN.value()
            # Generate sample data

            # Update the plot with the scaled data
            self.animated_widget1.ax.set_xlim(0,scale_x/10)
            self.animated_widget1.ax.set_ylim((scale_yn/100)*-1,scale_yp/100)
            self.animated_widget2.ax.set_xlim(0,scale_x/10)
            self.animated_widget2.ax.set_ylim((scale_yn/100)*-1,scale_yp/100)
            # Redraw the plot
            # self.animated_widget1.canvas.draw()

            
        except Exception as e:
            msgPrint(str(e))




