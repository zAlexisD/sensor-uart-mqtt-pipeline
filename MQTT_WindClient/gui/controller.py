"""
GUI Module for logic methods between UI and MQTT Client 
"""
from typing import Any
from queue import Queue,Full,Empty
from utils.config import infoTopics,statusTopics,LogQueue
import time

# Take data from on_message MQTT callback
def guiGetData(buffer:Queue,topic:str,data:Any):
    try:
        buffer.put((topic,data))
    except Full:
        addToLog(f"Tried to add ({topic},{data}) but buffer is full")

# Update method for measures, status and timestamp
def guiUpdateData(buffer:Queue):
    try:
        topic,data = buffer.get()
        if (topic in infoTopics) or (topic in statusTopics):
            return topic,data.decode()
        if topic == "Timestamp":
            return topic,int(data.decode())
    except Empty:
        addToLog(f"Tried to extract data but buffer is empty")

#TODO: Handle timestamps

# Handle log data
def addToLog(errorLog:str,logQueue:Queue=LogQueue):
    logQueue.put(f"{time.time()}: " + errorLog)