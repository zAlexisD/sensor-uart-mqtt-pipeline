"""
Widget Module for ADC Temperature info display
"""
from PyQt6.QtWidgets import QWidget,QLabel,QGridLayout
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np

class TemperatureWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):

        layout = QGridLayout()

        # --- Values display --- #
        self.label = QLabel("ADC Temperature: -- °C")
        self.label.setStyleSheet("font-size: 32px;")
        layout.addWidget(self.label,0,0,alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Live Graph settings --- #
        self.plot = pg.PlotWidget()
        # Font format
        self.plot.setBackground("k")
        self.plot.setTitle(
            "ADC Temperature", color="w", size="14pt"
        )
        self.plot.setLabel("left", "Temperature (°C)")
        self.plot.setLabel("bottom", "Time (samples)")
        self.plot.showGrid(x=True, y=True)
        # Inititate Arrays
        self.windRange = 10
        self.x = np.arange(self.windRange)
        #TODO: check how to initiate Y axis differently 
        self.y = np.zeros(self.windRange)

        # Plotline creation with referance
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.curve = self.plot.plot(self.x,self.y,pen=pen)

        # Add to layout
        layout.addWidget(self.plot,1,0)

        self.setLayout(layout)
    
    def update_data(self,value):
        # Update widget
        self.label.setText(f"ADC Temperature: {value}°C")

        # Update live plot by enabling scrolling effect
        self.x = np.roll(self.x, -1)    
        self.x[-1] = self.x[-2] + 1          # Scroll the x-axis forward.
        self.y = np.roll(self.y, -1)
        self.y[-1] = value                   # Add a new data point
        self.curve.setData(self.x, self.y)   # Redraw the line with updated data.