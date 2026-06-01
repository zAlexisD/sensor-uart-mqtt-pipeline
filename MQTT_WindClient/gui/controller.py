"""
GUI Module for logic methods between UI and MQTT Client 
"""
from typing import Any
from queue import Queue,Full,Empty
from MQTT_WindClient.mqtt.config import infoTopics,statusTopics

# Take data from on_message MQTT callback
def guiGetData(buffer:Queue,topic:str,data:Any):
    try:
        buffer.put((topic,data))
    except Full:
        #TODO: might add Log display on screen
        print("Buffer is full")

# Update method only applies for temperature and battery level
def guiUpdateData(buffer:Queue):
    try:
        topic,data = buffer.get()
        if topic in infoTopics:
            return topic,data
    except Empty:
        #TODO:LOG display
        print("Buffer is empty")

# Handle config data management
def guiGetConfig(buffer:Queue):
    try:
        configName,dictData = buffer.get()
        if configName not in infoTopics and configName not in statusTopics:
            return configName,dictData
    except Empty:
        #TODO:LOG display
        print("Buffer is empty")