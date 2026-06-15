"""
Screen Module for Configuration data popup
"""
from PyQt6.QtWidgets import QWidget,QGridLayout
from json import load,JSONDecodeError

from utils.config import sessionID
from gui.widgets.configWidget import ConfigWidget
from gui.controller import addToLog

#TODO: handle for any config type, not explicitly like this

class ConfigWindow(QWidget):
    def __init__(self,configList:list):
        super().__init__()
        self.configList = configList
        
        self.setWindowTitle("Configurations")

        configLayout = QGridLayout()

        # Load config if exists and create corresponding widgets
        configPath = f"data/config_{sessionID}.json"
        try:
            with open(configPath,"r",encoding="utf-8") as file:
                configs = load(file)
                # Init config widgets class
                self.devConfig  = ConfigWidget("DeviceInfo",configs["DeviceInfo"])
                self.rangParams = ConfigWidget("RangingParameter",configs["RangingParameter"])
                # Add to window
                configLayout.addWidget(self.devConfig,0,0)
                configLayout.addWidget(self.rangParams,0,1)
                
                self.setLayout(configLayout)

        except FileNotFoundError:
            addToLog("Error loading JSON: File not found")
        except JSONDecodeError as e:
            addToLog(f"Error decoding JSON: {e}")