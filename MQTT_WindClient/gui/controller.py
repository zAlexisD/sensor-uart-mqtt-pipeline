"""
GUI Module for logic methods between UI and MQTT Client 
"""
from typing import Any
from queue import Queue,Full,Empty
from MQTT_WindClient.mqtt.config import infoTopics,LogQueue
import time

# Take data from on_message MQTT callback
def guiGetData(buffer:Queue,topic:str,data:Any):
    try:
        buffer.put((topic,data))
    except Full:
        addToLog(f"Tried to add ({topic},{data}) but buffer is full")

# Update method only applies for temperature and battery level
def guiUpdateData(buffer:Queue):
    try:
        topic,data = buffer.get()
        if topic in infoTopics:
            return topic,data.decode()
    except Empty:
        addToLog(f"Tried to extract data but buffer is empty")

#TODO: Handle status data

# Handle log data
def addToLog(errorLog:str,logQueue:Queue=LogQueue):
    logQueue.put(f"{time.time()}: " + errorLog)