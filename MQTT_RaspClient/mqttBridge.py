"""
MQTT Application script - Publisher Client and MQTT-UART Bridge
"""
from getpass import getpass

from mqtt.helpers import *
from uart.uartReader import UARTReader
from uart.parser import UARTParser

#TODO: waiting for uart signals method ?
#TODO: can add more layouts

def mqttPubStart(broIP:str,broPort:int,userName:str,userPwd:str,serialP:str,baud:int):
    mqttc = newClient(brokIP=broIP,brokPort=broPort,cliUser=userName,cliPwd=userPwd)
    reader = UARTReader(port=serialP,baud=baud)
    parser = UARTParser()

    try:
        loopSession(mqttc,reader,parser)
    except KeyboardInterrupt:
        # Handle cleanly CTRL+C
        print("Stopped by user, disconnecting...")
        mqttc.disconnect()
        print("MQTT connection closed")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    args = checkArgs()
    # Check if user asks for private password typing
    if args.ask_pwd:
        args.pwd = getpass("Password: ")
    # Launch MQTT client
    mqttPubStart(args.ip,args.port,args.user,args.pwd,args.serialP,args.baud)