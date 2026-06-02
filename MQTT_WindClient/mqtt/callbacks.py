"""
MQTT Module for API Callbacks
"""
from mqtt.config import sessionID,MAX_PAYLOAD_SIZE,buffer
from mqtt.handlers import saveToJson
from gui.controller import guiGetData,addToLog

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"ERR: Broker rejected you subscription: {reason_code_list[0]}")
        addToLog(f"Sub failed -> {reason_code_list[0]}")
    else:
        print("[INFO] Subscription succeded")
        print(f"[INFO] Broker granted the following QoS: {reason_code_list[0].value}")


#TODO: might want to remove the disconnect part if we unsubscribe from some topic but not all
def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("[INFO] Unsubscription succeeded")
    else:
        print(f"ERR: Broker replied with failure: {reason_code_list[0]}")
        addToLog(f"Unsub failed -> {reason_code_list[0]}")
    # client.disconnect()

def on_message(client, userdata, message):
    msgPayload = message.payload
    size = len(msgPayload)
    msgTopic    = message.topic
    msgContent  = msgPayload.decode()
    
    if size > MAX_PAYLOAD_SIZE:
        print(f"Dropped MQTT message: payload too large: {size} bytes")
        addToLog(f"{msgTopic}-> too large ({size} B)")
        return

    #TODO: Migth make display simpler to avoir overloading command window
    print(f"\n[PUB] Received from topic `{msgTopic}`: `{msgContent}`")

    guiGetData(buffer,msgTopic,msgPayload)
    saveToJson(topic = msgTopic,data = msgContent)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"ERR: Failed to connect: {reason_code}. Retry connection")
        addToLog(f"Connect failed -> {reason_code}")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        print(f"\n[INFO] Connected to MQTT Broker! Session ID: {sessionID}")
        #TODO: might remove subscription here to let user chose
        # client.subscribe(topicList)

def on_log(client, userdata, level, buf):
    print("LOG:", buf)