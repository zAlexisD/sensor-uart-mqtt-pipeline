"""
Screen Module for main page of GUI
"""
from PyQt6.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QScrollArea
from PyQt6 import QtCore
import random
import numpy as np
from time import time,strftime,gmtime

from mqtt.handlers import TopicSelectController
from gui.widgets.batWidget import BatteryWidget
from gui.widgets.tempWidget import TemperatureWidget
from gui.widgets.logWidget import LogWidget
from gui.screens.configScreen import ConfigWindow
from gui.widgets.textWidget import TextWidget
from gui.widgets.statusWidget import StatusWidget
from gui.controller import guiUpdateData
from utils.config import buffer,infoTopics,configTopics,statusTopics,topicList

#TODO: Handle widgets to show according to chosen topics (if customed/initials)

class DashboardPage(QWidget):
    def __init__(self,controller:TopicSelectController,logs:bool=False):
        super().__init__()
        self.enableLog = logs
        self.controller = controller
        self.topics = self.controller.get_selected_topics()
        
        self.config = []
        self.infos = []
        self.status = []
        self.customs = []
        self.trackTime = False

        self.setWindowTitle("MQTT GUI Application")
        self.setStyleSheet("background-color: #514A6A")

        # Handle incoming topic list and set window size
        self.topicHandler()
        
        # Set widgets on the window grid
        self.mainLayout = QVBoxLayout()
        self.dataLayout = QHBoxLayout()
        self.sideLayout = QHBoxLayout()

        # Config widgets
        if self.config :    # check not empty
            self.setConfigWidget()
        # Measurements widgets
        if self.infos:  
            self.setInfoWidget()

        self.mainLayout.addLayout(self.dataLayout)
        
        # Customs widgets
        if self.customs:
            self.setCustomWidgets()

        # Status widgets
        if self.status:
            self.setStatusWidgets()
        # Log Widget
        if self.enableLog:
            self.setLogWidget()
        self.mainLayout.addLayout(self.sideLayout)

        self.setLayout(self.mainLayout)

        # Set up a timer to update the plots
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)  # 500ms = 2 updates per second
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    # Helper to assign topic names to their corresponding widget type
    def topicHandler(self):
        for topic in self.topics:
            # First handle measures cases
            if topic in infoTopics:
                self.infos.append(topic)
            # Then handle config case
            if topic in configTopics:
                self.config.append(topic)
            # Handle status
            if topic in statusTopics:
                self.status.append(topic)
            # Handle timestamp topic
            if topic == "Timestamp":
                self.trackTime = True
            # Remaining customs
            if topic not in topicList:
                self.customs.append(topic)

    # Config widget handler
    def setConfigWidget(self):
        configLayout = QHBoxLayout()
        # Set up button to display popup config window
        showConfig = QPushButton("Show Config",self.config)
        showConfig.clicked.connect(self.openConfig)
        configLayout.addWidget(showConfig)
        configLayout.addStretch()
        self.mainLayout.addLayout(configLayout)
        
    # Handler define measures widget
    def setInfoWidget(self):
        # Measurement info widgets
        for topic in self.infos:
            if topic == "ADCTemperature":
                self.temp = TemperatureWidget()
                self.temp.setMinimumSize(400, 300)
                self.dataLayout.addWidget(self.temp)
            else:
                self.bat = BatteryWidget()
                self.bat.setMinimumSize(400, 300)
                self.dataLayout.addWidget(self.bat)
    
    # Handler for status widgets
    def setStatusWidgets(self):
        self.statusWidget = StatusWidget(self.status)
        self.statusWidget.setMinimumHeight(170)
        self.sideLayout.addWidget(self.statusWidget)

    # Handler for customed widgets
    def setCustomWidgets(self):
        self.textWidget = TextWidget(self.customs)
        self.textWidget.setMinimumWidth(400)
        self.dataLayout.addWidget(self.textWidget)

    # Handler for logs widget
    def setLogWidget(self):
        self.logs = LogWidget()
        self.logs.setMinimumHeight(200)
        self.sideLayout.addWidget(self.logs)

    def update_data(self):
        # --- Test updates --- #
        # Generate sample timestamp for test
        timeValue = ""
        if self.trackTime:
            #TODO: see how to compact the timestamp -> not really important here as it is a test
            timeValue = strftime("%d%m%Y-%H:%M:%S ",gmtime(time()))
        #TODO: See how to update timestamp as dynamic plots x-axis
        # Update Temp, Battery, status if exist
        if self.infos or self.status:
            for topic in self.infos:
                random.seed(42)
                if topic == "ADCTemperature":
                    tempValue = np.random.randint(20, 60)
                    self.temp.update_data(tempValue)
                else:
                    batValue = np.random.randint(80, 100)
                    self.bat.update_data(batValue)
            for topic in self.status:
                random.seed(None)
                statusValue = random.choice(["Success","Failure","No Data"])
                self.statusWidget.update_data(topic,statusValue,timeValue)

        # Update status and customs if exist
        if self.customs:
            # # Initial test
            # self.textWidget.update_data(["Apple Caramel","Strawberry","Peach","Mango"])
            # Test with actual function
            for topic in self.customs:
                random.seed(None)
                statusValue = random.choice(["Apple Caramel","Strawberry","Peach","Mango"])
                self.textWidget.update_data(topic,statusValue)
        
        # Update test the log widget
        if self.enableLog:
            random.seed(None)
            logValue = random.choice(["Action Failed","Wrong Credentials",
                                      "Topic not found","Buffer overloaded"])
            self.logs.update_entry(logValue,timeValue)

        #TODO: Handle MQTT for status, timestamp and custom
        # # --- Connection with MQTT client to update values --- #
        # try:
        #   topic,value = guiUpdateData(buffer)
        #   if topic == "ADCTemperature":
        #       self.temp.update_data(value)
        #   if topic == "BatteryLevel":
        #       self.bat.update_data(value)
        #   if topic in self.status:
        #       self.statusWidget.update_data(topic,value)
        #   if topic in self.customs:
        #       self.textWidget.update_data(topic,value)
        #NOTE: defined like this, at each update might not update all status and widgets
        # -> would need for loops or explicitly handle each case

    # Config window popup properties
    def openConfig(self):
        if not hasattr(self):
            self.configWind = ConfigWindow()
        self.configWind.show()
        self.configWind.raise_()
        self.configWind.activateWindow()