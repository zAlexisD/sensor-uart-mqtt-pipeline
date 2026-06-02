"""
Screen Module for main page of GUI
"""
from PyQt6.QtWidgets import QWidget,QGridLayout
from widgets.batWidget import BatteryWidget
from widgets.configWidget import ConfigWidget
from widgets.tempWidget import TemperatureWidget
from PyQt6 import QtCore
# import random
# import numpy as np
from controller import guiUpdateData,addToLog
from json import load,JSONDecodeError
from mqtt.config import sessionID,buffer

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MQTT GUI Application")
        self.setStyleSheet("background-color: #514A6A")

        # Define all different widgets
        self.temp    = TemperatureWidget()
        self.battery = BatteryWidget()

        # Set widgets on the window grid
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.temp,0,0)
        mainLayout.addWidget(self.battery,0,1)

        # Load config if exists and create corresponding widgets
        configPath = f"data/config_{sessionID}.json"
        try:
            with open(configPath,"r",encoding="utf-8") as file:
                configs = load(file)
                # Init config widgets class
                self.devConfig  = ConfigWidget("DeviceInfo",configs["DeviceInfo"])
                self.rangParams = ConfigWidget("RangingParameter",configs["RangingParameter"])
                # Add to window
                mainLayout.addWidget(self.devConfig,0,2)
                mainLayout.addWidget(self.rangParams,0,3)
        except FileNotFoundError:
            addToLog("Error loading JSON: File not found")
        except JSONDecodeError as e:
            addToLog(f"Error decoding JSON: {e}")

        self.setLayout(mainLayout)

        # Set up a timer to update the plots
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)  # 500ms = 2 updates per second
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

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