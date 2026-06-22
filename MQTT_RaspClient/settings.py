"""
MQTT and Serial settings
"""
import random
import os
from dotenv import load_dotenv

# ========== MQTT settings ========== #
brokerIP = "192.168.1.115"
brokerPort = 1883
# Set of topics set at $SYS/# for all topics within broker
wholeList = "$SYS/#"
# For specific topics -> tuples [("topic1",qos=0 default),("topic2",qos),etc]
# topicList = ["testTopic"]

load_dotenv()  # loads .env automatically

clientID = f'publish-{random.randint(0, 100)}'
clientUsername = "mqttPublisher"
clientPwd = os.getenv("MQTT_PWD")

# ========== UART settings ========== #
# tagCOM  = "/dev/ttyUSB0"     # If Linux
tagCOM  = "COM4"             # IF Windows
tagBaud = 300000
tagData = {}