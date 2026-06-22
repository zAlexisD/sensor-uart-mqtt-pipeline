"""
Module for helpers definition
"""
import paho.mqtt.client as mqtt
from settings import *
from mqtt.callbacks import *
from uart.uartReader import UARTReader
from uart.parser import UARTParser
import argparse

#TODO: Handle other broker
def newClient(brokIP:str = brokerIP, brokPort:int = brokerPort,
              cliUser:str = "", cliPwd:str = "",
              enableAuths:bool=False,logs: bool = False) -> mqtt:
    # Use default credentials only if using our custom broker
    if brokIP == brokerIP:
        enableAuths = True
        cliUser = clientUsername
        cliPwd  = clientPwd
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,client_id=clientID)
    # Handle if authentification needed
    if enableAuths:
        mqttc.username_pw_set(cliUser,cliPwd)
    # Enable logs in commande window if precised
    if logs:
        mqttc.on_log = on_log

    mqttc.on_connect = on_connect
    print("[REQ] Connecting...")
    mqttc.connect(brokIP,brokPort)
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
            # print(f"Line: {line}")      # Debug
            if not line:
                continue

            parsed = parser.parse(line)
            # print(f"Parse: {parsed}")   # Debug
            if not parsed:
                continue

            # data.update(parsed)
            publishData(client,parsed)

        except Exception as e:
            print(f"Error: {e}")
            break
    client.loop_stop()

# Check user arguments
def checkArgs():
    parser = argparse.ArgumentParser(description="MQTT Client")

    # Serial Port arguments
    parser.add_argument("--serialP",type=str,
                        help="Serial Port on which the sensor device is connected")
    parser.add_argument("--baud",type=int,help="Serial baudrate")

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
    parser.add_argument("--ask_pwd", action="store_true",
                    help="Prompt for password securely")
    
    return parser.parse_args()