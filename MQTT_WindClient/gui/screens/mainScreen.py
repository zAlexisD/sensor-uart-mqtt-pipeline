"""
Screen Module for main page of GUI
"""
from PyQt6.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QScrollArea
from PyQt6 import QtCore
import random
import numpy as np
from time import time,strftime,gmtime
from typing import Any

from mqtt.handlers import TopicSelectController
from gui.widgets.batWidget import BatteryWidget
from gui.widgets.tempWidget import TemperatureWidget
from gui.widgets.logWidget import LogWidget
from gui.screens.configScreen import ConfigWindow
from gui.widgets.textWidget import TextWidget
from gui.widgets.statusWidget import StatusWidget
from gui.controller import guiUpdateData,addToLog
from utils.config import buffer,infoTopics,configTopics,statusTopics,topicList
from gui.screens.updateTopicScreen import TopicWindow

#TODO: Handle datatypes -> one widget helper for each type of display and its update method

class DashboardPage(QWidget):
    def __init__(self,controller:TopicSelectController,close_callback,logs:bool=False):
        super().__init__()
        self.closeAll       = close_callback
        self.enableLog      = logs
        self.controller     = controller

        self.trackTime = False

        # Dictionary of (topic category, list[{topic name: widget}])
        self.current_topics = {
            "Info":   [],
            "Config": [],
            "Status": [],
            "Other":  []
        }

        self.fct_dict = {
            "Info":   self.setInfoWidget,
            "Config": self.setConfigWidget,
            "Status": self.setStatusWidgets,
            "Other":  self.setCustomWidgets
        }

        self.setWindowTitle("MQTT GUI Application")
        self.setStyleSheet("background-color: #514A6A")

        # Assign widget type for each initial topic
        for topic in self.controller.get_selected_topics():
            self.topicHandler(topic)
        
        # Set widgets on the window grid
        self.mainLayout = QVBoxLayout()
        self.butnLayout = QHBoxLayout()
        self.dataLayout = QHBoxLayout()
        self.sideLayout = QHBoxLayout()

        # Set a dictionary of layout for update use
        self.layout_dict = {
            "Info":   self.dataLayout,
            #TODO: for config -> want to access layout within configWindow
            "Config": self.butnLayout,
            "Status": self.sideLayout,
            "Other":  self.dataLayout
        }

        # Set up top bar buttons
        self.setButtonsBar()

        # Measurements widgets
        if self.current_topics["Info"]:              # check not empty
            self.setInfoWidget()

        self.mainLayout.addLayout(self.dataLayout)
        
        # Customs widgets
        if  self.current_topics["Other"]:
            self.setCustomWidgets()

        # Status widgets
        if  self.current_topics["Status"]:
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
    def topicHandler(self,topic,isReturning:bool=False):
        # First handle measures cases
        if topic in infoTopics:
            self.current_topics["Info"].append({topic: None})
            return "Info" if isReturning else None
        # Then handle config case
        elif topic in configTopics:
            self.current_topics["Config"].append({topic: None})
            return "Config" if isReturning else None
        # Handle status
        elif topic in statusTopics:
            self.current_topics["Status"].append({topic: None})
            return "Status" if isReturning else None
        # Handle timestamp topic
        elif topic == "Timestamp":
            self.trackTime = True
            return "Time" if isReturning else None
        # Remaining customs
        else:
            self.current_topics["Other"].append({topic: None})
            return "Other" if isReturning else None
        
    # Define widget for whole list at init
    def setAllWidgets(self,widget_type):
        if self.current_topics[widget_type]:
            for item in self.current_topics[widget_type]:
                for key in item:
                    self.fct_dict[widget_type](key)

    # Config widget handler
    def setConfigWidget(self,topic):
        # Set up button to display popup config window
        showConfig = QPushButton("Show Config")
        showConfig.clicked.connect(self.openConfig)
        self.butnLayout.addWidget(showConfig)

    # Top bar button handler
    def setButtonsBar(self):
        # Config widgets
        self.setAllWidgets("Config")

        self.butnLayout.addStretch()
        # Reselect topics button
        self.update_btn = QPushButton("Update Topics")
        self.update_btn.clicked.connect(self.on_update_btn)
        self.butnLayout.addWidget(self.update_btn)
        # GUI closing button
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.closeAll)
        self.butnLayout.addWidget(self.close_btn)

        self.mainLayout.addLayout(self.butnLayout)
        
    # Handler define measures widget -> for numerical values
    #TODO: define a single widget for numerical data
    def setInfoWidget(self,topic:str):
        if topic == "ADCTemperature":
            self.temp = TemperatureWidget()
            self.temp.setMinimumSize(400, 300)
            self.dataLayout.addWidget(self.temp)
            self.current_topics["Info"][topic] = self.temp
        elif topic == "BatteryLevel":
            self.bat = BatteryWidget()
            self.bat.setMinimumSize(400, 300)
            self.dataLayout.addWidget(self.bat)
            self.current_topics["Info"][topic] = self.bat
        else:
            infoWidget: QWidget
            infoWidget.setMinimumSize(400,300)
            self.dataLayout.addWidget(infoWidget)
            self.current_topics["Info"][topic] = infoWidget
    
    # Handler for status widgets
    #TODO: similarly to config, update the status part directly with status widget
    def setStatusWidgets(self):
        self.statusWidget = StatusWidget(self.status)
        self.statusWidget.setMinimumHeight(170)
        self.sideLayout.addWidget(self.statusWidget)

    # Handler for customed widgets
    #TODO: dissociate text and numerical datatype -> but how to know datatype ?
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
        # # --- Test updates --- #
        # # Generate sample timestamp for test
        # timeValue = ""
        # if self.trackTime:
        #     #TODO: see how to compact the timestamp -> not really important here as it is a test
        #     timeValue = strftime("%d%m%Y-%H:%M:%S ",gmtime(time()))
        # #TODO: See how to update timestamp as dynamic plots x-axis
        # # Update Temp, Battery, status if exist
        # if self.infos or self.status:
        #     for topic in self.infos:
        #         random.seed(42)
        #         if topic == "ADCTemperature":
        #             tempValue = np.random.randint(20, 60)
        #             self.temp.update_data(tempValue)
        #         else:
        #             batValue = np.random.randint(80, 100)
        #             self.bat.update_data(batValue)
        #     for topic in self.status:
        #         random.seed(None)
        #         statusValue = random.choice(["Success","Failure","No Data"])
        #         self.statusWidget.update_data(topic,statusValue,timeValue)

        # # Update status and customs if exist
        # if self.customs:
        #     # # Initial test
        #     # self.textWidget.update_data(["Apple Caramel","Strawberry","Peach","Mango"])
        #     # Test with actual function
        #     for topic in self.customs:
        #         random.seed(None)
        #         statusValue = random.choice(["Apple Caramel","Strawberry","Peach","Mango"])
        #         self.textWidget.update_data(topic,statusValue)
        
        # # Update test the log widget
        # if self.enableLog:
        #     random.seed(None)
        #     logValue = random.choice(["Action Failed","Wrong Credentials",
        #                               "Topic not found","Buffer overloaded"])
        #     self.logs.update_entry(logValue,timeValue)

        #TODO: Handle MQTT for status, timestamp and custom
        # --- Connection with MQTT client to update values --- #
        try:
          # Try extract data
          topic,value = guiUpdateData(buffer)
          # Init timestamp value
          timeValue = ""
          if topic == "Timestamp":
              timeValue = value
          # Get data depending on topic
          elif topic == "ADCTemperature":
              self.temp.update_data(value)
          elif topic == "BatteryLevel":
              self.bat.update_data(value)
          elif topic in self.status:
              self.statusWidget.update_data(topic,value,timeValue)
          elif topic in self.customs:
              self.textWidget.update_data(topic,value)
        except Exception as e:
            addToLog(f"Update GUI data error: {e}")
        #NOTE: defined like this, at each update might not update all status and widgets
        # -> would need for loops or explicitly handle each case

    # Config popup window properties
    def openConfig(self):
        if not hasattr(self):
            #TODO: adjust config widget so that it can access the current topics and save the widget
            self.configWind = ConfigWindow(self.configs,self.current_topics)
        self.configWind.show()
        self.configWind.raise_()
        self.configWind.activateWindow()

    # Topic update popup window
    def on_update_btn(self):
        self.updateWindow = TopicWindow(self.topics)
        self.updateWindow.topic_update.connect(self.on_topic_updated)
        self.updateWindow.show()
        self.updateWindow.raise_()
        self.updateWindow.activateWindow()

    # Callback for topic updating
    def on_topic_updated(self,topic,state):
        # Assign to widget type
        #TODO: if config -> update in config popup window, not dashboard -> with configWind own method?
        widget_type = self.topicHandler(topic,isReturning=True)
        # Case unchecked -> state = 0
        if not state:
            self.remove_widget(topic,widget_type)
        # Case checked -> state = 2
        else:
            self.add_widget(topic,widget_type)

    # Add widget helper after initialization
    #TODO: handle datatypes
    def add_widget(self,topic,widget_type):
        # Check it is not already there -> weird case: checkbox would be already checked
        # but let's just keep it just in case
        if topic in self.current_topics[widget_type]:
            return
        # Create widget depending on datatype
        widget = self.fct_dict[widget_type](topic)
        self.current_topics[widget_type].append({topic: widget})

    # Remove widget after initialization
    def remove_widget(self,topic,widget_type):
        # if topic already not there -> also weird: checkbox would not be checked before
        if topic not in self.current_topics[widget_type]:
            return
        #TODO: if want to remove widget -> might need to store widgets in dictionary for e.g.
        # Remove widget from layout
        widget = self.current_topics[widget_type][topic]
        self.layout_dict[widget_type].removeWidget(widget)
        # Remove from current topics
        self.current_topics[widget_type]= [
            item for item in self.current_topics[widget_type]
            if topic not in item
        ]