"""
MQTT Module for logic handling
"""
from typing import Any
import json
from mqtt.config import topicList,sessionID,msgCount,timeTrack,infoTopics
import os

#TODO: topic selection handler
# def selectTopic():
    
#     for topic in topicList:
#         print(f"")
#     indexTopic = input("Which?")
#     return


#TODO: log handler?

# Init the json file as a dictionary with topics as key
def initJson(defaultValue:Any,topicList:list[str]=topicList) -> dict[str,Any]:
    return {key: defaultValue for key in topicList}

# Datatype handler for on_message callback -> actually convert back into dictionaries
def processData(topic:str,data:Any):
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
def storeData(dataDict: dict,filepath:str):
    with open(filepath,"w",encoding='utf-8') as f:
        json.dump(dataDict,f,indent=4)

# Update json file method to store every data from same session in one file
def saveToJson(topic:str,data:Any,sessionID:int=sessionID):
    jsonPath = f"data/{sessionID}.json"
    try:
        # Load this file or create it if it does not exist yet
        if os.path.exists(jsonPath):
            with open(jsonPath, 'r', encoding='utf-8') as f:
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
        
        # Process data and merge with the loaded one
        case,processedData = processData(topic,data)
        if case == "Info":
            loaded.setdefault(topic,[]).append(processedData)
        elif case == "Config/Status":
            loaded.update(processedData)
        
        # Save the file again
        storeData(loaded,jsonPath)
        print("Saved") #For Debug only

    except Exception as e:
        print(f"Error updating JSON file: {e}")