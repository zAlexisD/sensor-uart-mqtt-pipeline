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
        # self.time = []
        self.customs = []
        self.window_nb = 0

        self.setWindowTitle("MQTT GUI Application")
        self.setStyleSheet("background-color: #514A6A")

        # Handle incoming topic list and set window size
        self.topicHandler()
        self.widgetSize = self.countWindows()
        
        # Set widgets on the window grid
        self.mainLayout = QVBoxLayout()
        self.widgetLayout = QGridLayout()
        self.columnCount = 0

        # Config widgets
        if self.config :    # check not empty
            # Set up button to display popup config window
            showConfig = QPushButton("Show Config",self.config)
            showConfig.clicked.connect(self.openConfig)
            self.mainLayout.addWidget(showConfig)

        # Add measurements widgets
        if self.infos:  
            self.setInfoWidget()

        # Customs and status simple label widgets
        self.textLayout = QVBoxLayout()
        self.setStatusWidgets()
        self.setCustomWidgets()
        if self.status or self.customs:
            # Add widget only if at least one of previous topics exists
            self.widgetLayout.addLayout(self.textLayout,1,self.columnCount)
            self.columnCount += 1

        # Log Widget
        if self.enableLog:
            self.logs = LogWidget()
            self.logs.setFixedSize(self.widgetSize,400)
            self.widgetLayout.addWidget(self.logs,1,self.columnCount)

        self.mainLayout.addLayout(self.widgetLayout)
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
            #TODO: handle timestamp topic
            # Remaining customs
            if topic not in topicList:
                self.customs.append(topic)

    # Handler to preset number of windows to adapt dimensions
    def countWindows(self):
        if self.infos:
            self.window_nb += len(self.infos)
        if self.status or self.customs:
            self.window_nb += 1
        if self.enableLog:
            self.window_nb += 1
        return int(1200/self.window_nb)

    # Handler define measures widget
    def setInfoWidget(self):
        # Measurement info widgets
        for topic in self.infos:
            if topic == "ADCTemperature":
                self.temp = TemperatureWidget()
                self.temp.setFixedSize(self.widgetSize,400)
                self.widgetLayout.addWidget(self.temp,1,self.columnCount)
                self.columnCount += 1
            else:
                self.bat = BatteryWidget()
                self.bat.setFixedSize(self.widgetSize,400)
                self.widgetLayout.addWidget(self.bat,1,self.columnCount)
                self.columnCount += 1
    
    # Handler for status widgets
    def setStatusWidgets(self):
        if self.status:
            self.statusWidget = StatusWidget(self.status)
            self.statusWidget.setFixedSize(self.widgetSize,200)
            self.textLayout.addWidget(self.statusWidget)

    # Handler for customed widgets
    def setCustomWidgets(self):
        if self.customs:
            self.textWidget = TextWidget(self.customs)
            self.textWidget.setFixedSize(self.widgetSize,200)
            self.textLayout.addWidget(self.textWidget)

    def update_data(self):
        # --- Test updates --- #
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
                self.statusWidget.update_data(topic,statusValue)

        # Update status and customs if exist
        if self.customs:
            self.textWidget.update_data(["Apple Caramel","Strawberry","Peach","Mango"])
            #TODO: look how to take status valeus in MQTT -> read json ? from buffer?
        
        # Update test the log widget
        if self.enableLog:
            random.seed(None)
            logValue = random.choice(["Action Failed","Wrong Credentials",
                                      "Topic not found","Buffer overloaded"])
            self.logs.update_entry(logValue)

        #TODO: Handle MQTT for status, timestamp, custom and logs
        # # --- Connection with MQTT client to update values --- #
        # topic,value = guiUpdateData(buffer)
        # if topic == "ADCTemperature":
        #     self.temp.update_data(value)
        # else:
        #     self.bat.update_data(value)

    # Config window popup properties
    def openConfig(self):
        if not hasattr(self):
            self.configWind = ConfigWindow()
        self.configWind.show()
        self.configWind.raise_()
        self.configWind.activateWindow()