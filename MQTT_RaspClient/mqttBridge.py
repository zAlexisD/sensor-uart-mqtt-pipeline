"""
MQTT Application script - Publisher Client and MQTT-UART Bridge
"""
from mqtt.helpers import *
from uart.uartReader import UARTReader
from uart.parser import UARTParser

#TODO: waiting for uart signals method ?
#TODO: can add more layouts

def mqttPubStart():
    mqttc = newClient()
    reader = UARTReader()
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
    mqttPubStart()