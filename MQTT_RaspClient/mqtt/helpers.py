"""
Module for helpers definition
"""
import paho.mqtt.client as mqtt
from settings import *
from mqtt.callbacks import *
from uart.uartReader import UARTReader
from uart.parser import UARTParser

def newClient(logs: bool = False) -> mqtt:
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,client_id=clientID)
    mqttc.username_pw_set(clientUsername,clientPwd)
    # Enable logs in commande window if precised
    if logs:
        mqttc.on_log = on_log
    mqttc.on_connect = on_connect
    print("[REQ] Connecting...")
    mqttc.connect(brokerIP,brokerPort)
    return mqttc

def publishData(client: mqtt,data: dict = tagData):
    client.on_publish = on_publish
    for topic in data.keys():
        client.publish(topic,data[topic])
        #TODO: At first displaying a print is ok but for later we just need to send the data
        print(f"\n[REQ] Sending `{data[topic]}` to topic `{topic}`...")

def loopSession(client:mqtt,reader:UARTReader,parser:UARTParser,data:dict=tagData):
    client.loop_start()
    while True:
        try:
            line = reader.read_line()
            if not line:
                print(f"Line: {line}")
                continue
            parsed = parser.parse(line)
            if not parsed:
                print(f"Parse: {parsed}")
                continue
            data.update(parsed)
            publishData(client,data)
        except Exception as e:
            print(f"Error: {e}")
            break
    client.loop_stop()