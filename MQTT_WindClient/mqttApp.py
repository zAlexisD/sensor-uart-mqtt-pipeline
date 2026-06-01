"""
MQTT Application script - MQTT subscriber client in Windows
"""
from MQTT_ProjectFolder.mqttApp.mqtt.manager import *
from MQTT_ProjectFolder.mqttApp.mqtt.config import topicList
from MQTT_ProjectFolder.mqttApp.mqtt.layout import CONSOLE_HEADER

#TODO: Add user data selection choice (buttons? for GUI), (option1, option2, ..., various ones, all)
#TODO: Handle change of QoS ? -> might be useless we will only take QoS = 0
#TODO: Might add maximum listening time and/or max amount of data to store

def mqttSubStart():
    print(CONSOLE_HEADER)
    # MQTT Subscriber Client loop
    mqttc = newClient()
    reqSubscription(mqttc,topicList)

    try:
        loopSession(mqttc,topicList)
    except KeyboardInterrupt:
        # CTRL + C
        print("Stopped by user, disconnecting...")
        reqDisconnect(mqttc)
        print("MQTT connection closed")
    except Exception as e:
        print(f"Error: {e}")
        


#TODO: GUI: Open window, ask for user to start the MQTT subscription to launch and get data

if __name__ == "__main__":
    mqttSubStart()