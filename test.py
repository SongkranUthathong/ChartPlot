import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class AnimatedPlotWidget(QWidget):
    def __init__(self, parent=None):
        super(AnimatedPlotWidget, self).__init__(parent)
        self.j = 0
        # Create a Figure instance

        self.figure, self.ax = plt.subplots()
        # self.figure = Figure()

        # Create a FigureCanvasQTAgg instance
        self.canvas = FigureCanvas(self.figure)

        # Create an axis for the plot
        # self.ax = self.figure.add_subplot(111)

        # Initialize the plot data
        self.x = np.linspace(0, 2 * np.pi, 1000,)
        self.y = np.sin(self.x)

        # Create the plot line
        self.plot_line, = self.ax.plot(self.x, self.y,animated=True)

        self.ax.draw_artist(self.plot_line)

        # Create a timer to update the plot at regular intervals
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(10)  # Update the plot every 100 milliseconds

        # Create a layout for the widget and add the canvas to it
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plot(self):
        # Update the plot data
        self.y = np.sin(self.x + (self.j / 200) * np.pi)  # Simulate new data

        self.plot_line.set_ydata(self.y)
        self.ax.draw_artist(self.plot_line)
        self.canvas.blit(self.figure.bbox)
        self.canvas.flush_events()
        self.canvas.draw()
        
        self.j +=1

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Animated Plot Example")
        self.setGeometry(100, 100, 800, 600)

        # Create the animated plot widget
        animated_widget = AnimatedPlotWidget(self)

        # Add the animated plot widget to the main window
        layout = QVBoxLayout()
        layout.addWidget(animated_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
