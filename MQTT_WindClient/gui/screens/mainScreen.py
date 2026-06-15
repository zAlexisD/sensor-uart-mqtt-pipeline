"""
Screen Module for main page of GUI
"""
from PyQt6.QtWidgets import QWidget,QGridLayout,QPushButton,QVBoxLayout,QLabel
from PyQt6 import QtCore
import random
import numpy as np

from mqtt.handlers import TopicSelectController
from gui.widgets.batWidget import BatteryWidget
from gui.widgets.tempWidget import TemperatureWidget
from gui.widgets.logWidget import LogWidget
from gui.screens.configScreen import ConfigWindow
from gui.widgets.textWidget import TextWidget
from gui.controller import guiUpdateData
from utils.config import buffer,infoTopics,configTopics

#TODO: Handle widgets to show according to chosen topics (if customed/initials)

class DashboardPage(QWidget):
    def __init__(self,controller:TopicSelectController):
        super().__init__()
        self.controller = controller
        self.topics = self.controller.get_selected_topics()
        
        self.config = []
        self.infos = []
        self.customs = []

        self.setWindowTitle("MQTT GUI Application")
        self.setStyleSheet("background-color: #514A6A")

        # Define all different widgets
        self.topicHandler()
        
        # Set widgets on the window grid
        self.mainLayout = QVBoxLayout()
        self.widgetLayout = QGridLayout()
        self.columnCount = 0

        # Config widgets
        if self.config :
            # Set up button to display popup config window
            showConfig = QPushButton("Show Config",self.config)
            showConfig.clicked.connect(self.openConfig)
            self.mainLayout.addWidget(showConfig)

        # Add measurements widgets
        self.setInfoWidget()

        # Customs and status simple label widgets

        # Log Widget
        self.logs = LogWidget()
        self.widgetLayout.addWidget(self.logs,1,self.columnCount)

        self.mainLayout.addLayout(self.widgetLayout)
        self.setLayout(self.mainLayout)

    # Helper to assign topic names to their corresponding widget type
    def topicHandler(self):
        for topic in self.topics:
            # First handle measures cases
            if topic in infoTopics:
                self.infos.append(topic)
            # Then handle config case
            if topic in configTopics:
                self.config.append(topic)
            # Remaining includes status and customs, we treat them equally for now as there is no status widget type yet
            else:
                self.customs.append(topic)

    # Handler define measures widget
    def setInfoWidget(self):
        # Measurement info widgets
        if self.infos:  # check that it is not empty
            for topic in self.infos:
                if topic == "ADCTemperature":
                    self.temp = TemperatureWidget()
                    self.widgetLayout.addWidget(self.temp,1,self.columnCount)
                    self.columnCount += 1
                else:
                    self.bat = BatteryWidget()
                    self.widgetLayout.addWidget(self.bat,1,self.columnCount)
                    self.columnCount += 1

            # Set up a timer to update the plots
            self.timer = QtCore.QTimer()
            self.timer.setInterval(500)  # 500ms = 2 updates per second
            self.timer.timeout.connect(self.update_data)
            self.timer.start()
    
    # Handler for customed and status widgets
    def setCustomWidgets(self):
        if self.customs:
            customLayout = QVBoxLayout()
            for topic in self.customs:
                new_widget = TextWidget(topic)
                customLayout.addWidget(new_widget,1,self.columnCount)
                self.columnCount += 1

    def update_data(self):
        # Test values
        random.seed(42)
        tempValue = np.random.randint(20, 60)
        batValue = np.random.randint(80, 100)

        for topic in self.infos:
            if topic == "ADCTemperature":
                self.temp.update_data(tempValue)
            else:
                self.bat.update_data(batValue)

        # # Connection with MQTT client to update values
        # topic,value = guiUpdateData(buffer)
        # if topic == "ADCTemperature":
        #     self.temp.update_data(value)
        # else:
        #     self.battery.update_data(value)

    # Config window popup properties
    def openConfig(self):
        if not hasattr(self):
            self.configWind = ConfigWindow()
        self.configWind.show()
        self.configWind.raise_()
        self.configWind.activateWindow()