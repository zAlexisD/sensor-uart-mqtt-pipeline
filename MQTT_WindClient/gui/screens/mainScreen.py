"""
Screen Module for main page of GUI
"""
from PyQt6.QtWidgets import QWidget,QGridLayout,QPushButton
from widgets.batWidget import BatteryWidget
from widgets.tempWidget import TemperatureWidget
from widgets.logWidget import LogWidget
from PyQt6 import QtCore
from screens.configScreen import ConfigWindow
# import random
# import numpy as np
from controller import guiUpdateData
from mqtt.config import buffer

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MQTT GUI Application")
        self.setStyleSheet("background-color: #514A6A")

        # Define all different widgets
        self.temp    = TemperatureWidget()
        self.battery = BatteryWidget()
        self.logs    = LogWidget()

        # Set widgets on the window grid
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.temp,0,0)
        mainLayout.addWidget(self.battery,0,1)
        mainLayout.addWidget(self.logs,0,2)

        self.setLayout(mainLayout)

        # Set up a timer to update the plots
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)  # 500ms = 2 updates per second
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

        # Set up button to display popup config window
        self.showConfig = QPushButton("Show Config")
        self.showConfig.clicked.connect(self.openConfig)

    def update_data(self):
        # Update digits displays

        # test
        # random.seed(42)
        # tempValue = np.random.randint(20, 60)
        # batValue = np.random.randint(80, 100)

        # Connection with MQTT client to update values
        topic,value = guiUpdateData(buffer)
        if topic == "ADCTemperature":
            self.temp.update_data(value)
        else:
            self.battery.update_data(value)

    # Config window popup properties
    def openConfig(self):
        if not hasattr(self):
            self.configWind = ConfigWindow()
        self.configWind.show()
        self.configWind.raise_()
        self.configWind.activateWindow()