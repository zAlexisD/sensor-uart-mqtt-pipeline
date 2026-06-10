"""
MQTT Module for logic handling
"""
from typing import Any
import json
from utils.config import *
import os
from PyQt6.QtCore import QObject, pyqtSignal
from mqtt.manager import mqttSubStart
import argparse
import threading

#TODO: topic selection handler
class TopicSelectController(QObject):
    topic_selection = pyqtSignal(list)  # emits final topic list

    def __init__(self):
        self.selectedTopics  = []
        self.availableTopics = topicList
    
    # For CLI -> let the user input topics one by one for convenience
    # Loop until user inputs "ok"
    def set_topics_from_cli(self):
        print("Please select initial topic set, enter 'all' to add all, 'ok' when done\n")
        while True:
            topic = input("> ")
            if topic == "ok":
                break
            if topic == "all":
                self.selectedTopics = self.availableTopics.copy()
            else:
                # Let the user add even unkown topics, but might never get publishment
                #TODO: add small warning if unknown topics ?
                self.selectedTopics.append(topic)
                print(f"{topic} added\n")
        
        # Emit signal for consistency (even if GUI not used)
        self.topic_selection.emit(self.selectedTopics)
    
    # For GUI -> set logic will be done in corresponding PyQt class
    def set_topics_from_gui(self, topics):
        self.selectedTopics = topics
        self.topic_selection.emit(topics)

    def get_selected_topics(self):
        return self.selectedTopics
    
# Open separate thread for MQTT if GUI enabled
def startMqttThread(topics:list,broIP,broPort,userName,userPwd):
    # Launch thread for MQTT
    mqttThread = threading.Thread(target=mqttSubStart,
                                args=(broIP,broPort,userName,userPwd,topics),
                                daemon=True)
    mqttThread.start()

# Init the json file as a dictionary with topics as key
def initJson(defaultValue:Any,topicList:list[str]=topicList) -> dict[str,Any]:
    return {key: defaultValue for key in topicList}

# Datatype handler for on_message callback -> actually convert back into dictionaries
def processData(topic:str,data:Any):
    # Init msgCount if is empty
    if msgCount == {}:
        msgCount = initJson(0,topicList)
        
    # Update tracking count dictionary
    msgCount[topic] = msgCount.get(topic, 0) + 1
    
    # Handle Timestamp topic
    if topic == "Timestamp":
        timeTrack.append(data)
        return "Time",None
    
    # Handle Info topics (Temperature and Battery Level)
    if topic in infoTopics:
        # Update new dictionary values
        processedData = {
            "Message Count": msgCount[topic],
            "Value": data,
            # Last timestamp registered
            "Timestamp": timeTrack[-1]
        }
        return "Info",processedData

    # Others cases (Config or status that does not change) -> handled directly in saveToJson
    # As they only return the data, we do not need to update them
    else:
        return "Config/Status",{topic: data}

#TODO: Received data manager -> take to plot, store somewhere
def storeData(dataDict: Any,filepath:str):
    with open(filepath,"w",encoding='utf-8') as f:
        json.dump(dataDict,f,indent=4)

# Method to check if file exists, if not create + init it
def setupJson(path:str):
    # Load this file or create it if it does not exist yet
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                loaded = json.load(f)
                if not isinstance(loaded, dict):
                    print("Warning: JSON root is not a dictionary. Overwriting.")
                    loaded = initJson(defaultValue=[])
            except json.JSONDecodeError:
                print("Warning: JSON file is empty or invalid. Starting fresh.")
                loaded = initJson(defaultValue=[])
    else:
        loaded = initJson(defaultValue=[])
    
    return loaded

# Update json file method to store every data from same session in one file
def saveToJson(topic:str,data:Any,sessionID:int=sessionID):
    jsonPath = f"data/{sessionID}.json"
    try:
        # Load this file or create it if it does not exist yet
        loaded = setupJson(jsonPath)
        
        # Process data and merge with the loaded one
        case,processedData = processData(topic,data)
        if case == "Info":
            loaded.setdefault(topic,[]).append(processedData)
        # Save status in same file
        elif topic in statusTopics:
            loaded.update(processedData)
        # Handle case topic is Timestamp -> ignore
        elif topic == "Timestamp":
            return
        # Config case -> save in a specific file
        else:
            configPath = f"data/config_{sessionID}.json"
            loadConfig = setupJson(configPath)
            loadConfig.update(processData)
            storeData(loadConfig,configPath)
            return
        
        # Save the file again
        storeData(loaded,jsonPath)
        print("Saved") #For Debug only

    except Exception as e:
        print(f"Error updating JSON file: {e}")

def checkArgs():
    parser = argparse.ArgumentParser(description="MQTT Client")

    # GUI Flag -> set to True if --gui is passed
    parser.add_argument("--gui",action="store_true",help="Enable GUI Mode")

    # Broker connection parameters
    parser.add_argument("--ip",type=str,default=brokerIP,
                        help="MQTT Broker IP Address")
    parser.add_argument("--port",type=int,default=brokerPort,
                        help="MQTT Broker Port")
    parser.add_argument("--user",type=str,default=clientUsername,
                        help="MQTT client Username")
    parser.add_argument("--pwd",type=str,default=clientPwd,
                        help="MQTT client User Password")
    
    # Add argument to ask for password prompt to avoid displaying it
    parser.add_argument("--ask-pwd", action="store_true",
                    help="Prompt for password securely")
    
    return parser.parse_args()