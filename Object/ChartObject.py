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


class AnimatedPlotWidget(QWidget):
    def __init__(self, parent=None):
        super(AnimatedPlotWidget, self).__init__(parent)
        # Create a Figure instance
        self.figure, self.ax = plt.subplots()
        # self.figure = Figure()

        # Create a FigureCanvasQTAgg instance
        self.canvas = FigureCanvas(self.figure)
        # Initialize the plot data
        self.x = np.linspace(0, 5000,5000)
        # print(len(self.x))
        # self.y = np.sin(self.x)
        self.y = np.linspace(-2,0,5000)
        print(self.y)

        # Create the plot line
        self.plot_line, = self.ax.plot(self.x, self.y)

        self.ax.draw_artist(self.plot_line)
        

        # # Create a timer to update the plot at regular intervals
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_plot1)
        # self.timer.start(10)  # Update the plot every 100 milliseconds

        # # Create a layout for the widget and add the canvas to it
        # layout = QVBoxLayout()
        # layout.addWidget(self.canvas)
        # self.setLayout(layout)

class ForceTorqeChart(QMainWindow):
    def __init__(self,MainWindows):
        super().__init__()

        # Force Chart
        self.j = 0

        self.MainWindows = MainWindows

        self.animated_widget1 = AnimatedPlotWidget(self)

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



