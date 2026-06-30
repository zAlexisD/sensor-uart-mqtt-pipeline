"""
GUI Module for logic methods between UI and MQTT Client 
"""
from typing import Any
from queue import Queue,Full,Empty
from utils.config import configTopics,LogQueue
import time

# Take data from on_message MQTT callback
def guiGetData(buffer:Queue,topic:str,data:Any):
    try:
        buffer.put((topic,data))
    except Full:
        addToLog(f"Tried to add ({topic},{data}) but buffer is full")

# Update method for any data type except configuration
def guiUpdateData(buffer:Queue):
    try:
        topic,data = buffer.get()
        if topic not in configTopics:
            return topic,data.decode()
    except Empty:
        addToLog(f"Tried to extract data but buffer is empty")

# Handle log data
def addToLog(errorLog:str,logQueue:Queue=LogQueue):
    logQueue.put(f"{time.time()}: " + errorLog)