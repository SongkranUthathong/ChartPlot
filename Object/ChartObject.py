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


class CustomThread(QThread):

    signal = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super(CustomThread, self).__init__(parent)
        # self.rtde_r = rtde_receive.RTDEReceiveInterface("192.168.47.128")
        self.rtde_r = RTDEReceive("192.168.47.128")
        self.MAX = 5000
        self.FX = [0] * self.MAX
    def run(self):
        # This method will be executed in a separate thread
        while True:
            actual_q = self.rtde_r.getActualQ()
            for i in range(self.MAX):
                if i < self.MAX - 1:
                    self.FX[i] = self.FX[i+1]
                else:
                    self.FX[i] = actual_q[0]
                # print(i)
            
            time.sleep(1/100)  # Simulate a time-consuming operation
            self.signal.emit(np.array(self.FX))
        # self.signal.emit("Task completed!")
        # msgPrint("Task completed!")


class PlotProfile(QWidget):
    def __init__(self, parent=None):
        super(PlotProfile, self).__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.x = np.linspace(0, int(5000/100),5000)
        self.y = np.linspace(0,1,5000)
        # Create the plot line
        self.plot_line, = self.ax.plot(self.x, self.y)
        self.ax.draw_artist(self.plot_line)

class ForceTorqeChart(QMainWindow):
    def __init__(self,MainWindows):
        super().__init__()

        # Force Chart
        self.j = 0

        self.MainWindows = MainWindows

        self.animated_widget1 = PlotProfile(self)

        layout1 = QVBoxLayout()
        layout1.addWidget(self.animated_widget1.canvas)
        # # layout2 = QVBoxLayout()
        # # layout2.addWidget(animated_widget2)
        # # self.setCentralWidget(animated_widget)
        # # self.MainWindows.setCentralWidget(animated_widget)
        self.MainWindows.chart_Force.setLayout(layout1)

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
            self.animated_widget1.plot_line.set_ydata(FTSensor)

            self.animated_widget1.ax.draw_artist(self.animated_widget1.plot_line)
            self.animated_widget1.canvas.blit(self.animated_widget1.figure.bbox)
            self.animated_widget1.canvas.flush_events()
            self.animated_widget1.canvas.draw()
            self.j += 1
        except Exception as e:
            msgPrint(str(e))

    def addjust_Plort(self):
        try:
            pass
            scale_x = self.MainWindows.scaleX.value() / 100
            scale_y = self.MainWindows.scaleYP.value() / 100
            # Generate sample data
            x = np.linspace(self.MainWindows.scaleYN.value(), 100*scale_x, 5000)
            y = np.sin(x)

            # Update the plot with the scaled data
            self.animated_widget1.ax.clear()
            self.animated_widget1.ax.plot(x, y * scale_y)
            self.animated_widget1.ax.set_xlabel("X Axis")
            self.animated_widget1.ax.set_ylabel("Y Axis")

            # Redraw the plot
            self.animated_widget1.canvas.draw()
            
        except Exception as e:
            msgPrint(str(e))

    def scalueX_Adjust(self):
        try:
            __xScale = self.MainWindows.scaleX.value()
            msgPrint(self.MainWindows.scaleX.value())
            self.animated_widget1.x = np.linspace(0, int(__xScale/100),__xScale)
            self.animated_widget1.y = np.linspace(0,1,__xScale)

            print(self.animated_widget1.x)

            # self.animated_widget1.plot_line, = self.animated_widget1.ax.plot(self.animated_widget1.x, self.animated_widget1.y)

            # self.animated_widget1.plot_line.set_ydata(self.animated_widget1.y)
            self.animated_widget1.plot_line, = self.animated_widget1.ax.plot(self.animated_widget1.x, self.animated_widget1.y)

            self.animated_widget1.ax.draw_artist(self.animated_widget1.plot_line)
            self.animated_widget1.canvas.blit(self.animated_widget1.figure.bbox)
            self.animated_widget1.canvas.flush_events()
            self.animated_widget1.canvas.draw()
            pass
        except Exception as e:
            msgPrint(str(e))
    
    def scalueYP_Adjust(self):
        try:
            msgPrint(self.MainWindows.scaleYP.value())
            pass
        except Exception as e:
            msgPrint(str(e))

    def scalueYN_Adjust(self):
        try:
            msgPrint(self.MainWindows.scaleYN.value())
            pass
        except Exception as e:
            msgPrint(str(e))




