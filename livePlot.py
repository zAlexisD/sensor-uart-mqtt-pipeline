from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
import sys
import random

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-Time PyQtGraph Plot")

        layout = QtWidgets.QVBoxLayout()

        self.graphWidget = pg.PlotWidget()
        # self.setCentralWidget(self.graphWidget)

        # Configure the plot appearance.
        self.graphWidget.setBackground("w")
        self.graphWidget.setTitle(
            "Live Data", color="k", size="14pt"
        )
        self.graphWidget.setLabel("left", "Amplitude")
        self.graphWidget.setLabel("bottom", "Time (samples)")
        self.graphWidget.showGrid(x=True, y=True)
        layout.addWidget(self.graphWidget)

        # Add second window -> Last 30 seconds (Dezoom)
        self.graphDezoom = pg.PlotWidget()
        self.graphDezoom.setBackground("k")
        self.graphDezoom.setTitle(
            "Last 30 seconds",color="w",size="14pt"
        )
        self.graphDezoom.setLabel("left", "Amplitude")
        self.graphDezoom.setLabel("bottom", "Time (samples)")
        self.graphDezoom.showGrid(x=True, y=True)
        layout.addWidget(self.graphDezoom)

        # Container manage multi windows
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize data arrays.
        random.seed(42)
        self.buffer_size = 200
        self.x = np.arange(self.buffer_size)
        # self.y = np.zeros(self.buffer_size)
        self.y = np.random.randint(0, 100, 200)

        # Other data array for 2nd window
        self.x_long = np.arange(600)
        self.y_long = np.random.randint(0, 100, 600)

        # Create the plot line and keep a reference.
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.dataLine2 = self.graphDezoom.plot(self.x_long,self.y_long,pen=pen)

        # Set up a timer to update the plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)  # 50ms = 20 updates per second
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        random.seed(42)
        new_value = np.random.randint(0, 100)

        # Scroll the x-axis forward.
        self.x = np.roll(self.x, -1)
        self.x[-1] = self.x[-2] + 1
        # Add a new data point (replace with your data source).
        self.y = np.roll(self.y, -1)
        self.y[-1] = new_value
        # Redraw the line with updated data.
        self.data_line.setData(self.x, self.y)

        # Update 2nd window
        self.x_long = np.roll(self.x_long, -1)
        self.x_long[-1] = self.x_long[-2] + 1
        self.y_long = np.roll(self.y_long, -1)
        self.y_long[-1] = new_value
        self.dataLine2.setData(self.x_long, self.y_long)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())