"""
MQTT Module for configurations
"""
import random
import os
import dotenv
from datetime import datetime
from mqtt.handlers import initJson
import queue

brokerIP = "192.168.1.115"
brokerPort = 1883
# Set of topics set at $SYS/# for all topics within broker
wholeList = "$SYS/#"
# For specific topics -> tuples [("topic1",qos=0 default),("topic2",qos),etc]
# LEt's define the list of chosen topics
topicList = ["DeviceInfo","RangingParameter","UWBSessionstate","DeviceState",
             "Timestamp","ADCTemperature","BatteryLevel","phHbci"]
infoTopics = ["ADCTemperature","BatteryLevel"]
statusTopics = ["UWBSessionstate","DeviceState","phHbci"]

dotenv.load_dotenv()  # loads .env automatically

clientID = f'subscribe-{random.randint(0, 100)}'
clientUsername = "mqttSubscriber"
clientPwd = os.getenv("MQTT_PWD")

# Define maximum payload size
kiloByte = 1024
MAX_PAYLOAD_SIZE = 5 * kiloByte

# Define a session ID corresponding to MQTT session start time for data saving part
sessionID = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define a timestamp queue
timeTrack = []

# Track topics measures via a dictionary counting messages received for specific topic
# Initiated at 0, each time a message is received from a topic -> increase its count value of 1
msgCount = initJson(0,topicList)

# Define a buffer queue for MQTT-GUI bridging
buffer = queue.Queue(maxsize=300)