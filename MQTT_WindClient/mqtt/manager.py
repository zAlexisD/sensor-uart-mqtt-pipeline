"""
MQTT Module for helpers definition
"""
import paho.mqtt.client as mqtt
import threading

from utils.config import *
from mqtt.callbacks import *
from mqtt.layout import dispStatus,COMMANDS_HEADER,CONSOLE_HEADER

def newClient(brokIP:str = brokerIP, brokPort:int = brokerPort,
              cliUser:str = "", cliPwd:str = "",
              enableAuths:bool=False,logs:bool = False) -> mqtt:
    # Use default credentials only if using our custom broker
    if brokIP == brokerIP:
        enableAuths = True
        cliUser = clientUsername
        cliPwd  = clientPwd
    # Create a new MQTT Client
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,client_id=clientID)
    # Handle if authentification needed
    if enableAuths:
        mqttc.username_pw_set(cliUser,cliPwd)
    # Enable logs in commande window if precised
    if logs:
        mqttc.on_log = on_log

    mqttc.on_connect = on_connect
    print("[REQ] Connecting to Broker...")
    mqttc.connect(brokIP,brokPort)
    return mqttc

#TODO: manage topic selection (show available topics?), default for now : whole list
def reqSubscription(client: mqtt, topic: list = wholeList):
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    for top in topic:
        print(f"[REQ] Subscribing to topic `{top}`...")
        client.subscribe(top)

#TODO: manage topic selection, default for now : whole list
def reqUnsubscription(client: mqtt, topic: list = wholeList):
    client.on_unsubscribe = on_unsubscribe
    client.unsubscribe(topic)

def reqDisconnect(client: mqtt):
    reqUnsubscription(client) # Unsubscribe from all before disconnecting
    client.disconnect()

def loopSession(client: mqtt, topic: list = wholeList,guibool:bool=False):
    # Add 1st loop flag for correct print ordering and launching listening loop
    # guibool added to hommit this step if GUI enabled
    firstLoop = True if not guibool else False
    # Enable user inputs while listening for publications
    client.loop_start()
    while True:
        # The first loop returns on_connect and on_subscribe callbacks ouput before loop session
        if firstLoop:
            print("\n Press ENTER to start Listening session")
            input("")
            firstLoop = False
        else:
            try:
                dispStatus(client,topic)
                cmd = input("> ")
                #TODO: convert this in something more readable ?
                if cmd == "exit":
                    break
                elif cmd == "status":
                    print("Connected: ",client.is_connected())
                elif cmd == "help":
                    print(COMMANDS_HEADER)
                elif cmd == "topics":
                    print(topicList)

                elif cmd.startswith("unsub") or cmd.startswith("sub"):
                    cmdList = cmd.split(" ")
                    prefix,topicName = cmdList[0],cmdList[1]
                    if prefix == "unsub":
                        reqUnsubscription(client,topicName)
                        topic.remove(topicName)
                    elif prefix == "sub":
                        reqSubscription(client,[topicName])
                        topic.append(topicName)
                else:
                    print("Unrecognised command")
                
            except EOFError:
                # TODO: CTRL+D command not recognised
                # CTRL+D
                break
            except Exception as e:
                print(f"Error: {e}")
                break
            
    print("[REQ] Disconnecting...")
    reqDisconnect(client)
    print("[INFO] Disconnected")
    client.loop_stop()

def mqttSubStart(broIP:str,broPort:int,userName:str,userPwd:str,topics:list,guibool:bool):
    print(CONSOLE_HEADER)
    # MQTT Subscriber Client loop
    mqttc = newClient(brokIP=broIP,brokPort=broPort,cliUser=userName,cliPwd=userPwd)
    reqSubscription(mqttc,topics)

    try:
        loopSession(mqttc,topics,guibool)
    except KeyboardInterrupt:
        # CTRL + C
        print("Stopped by user, disconnecting...")
        reqDisconnect(mqttc)
        print("MQTT connection closed")
    except Exception as e:
        print(f"Error: {e}")

# Open separate thread for MQTT if GUI enabled
def startMqttThread(topics:list,broIP,broPort,userName,userPwd,guibool):
    # set Mqtt as main thread if CLI Mode, daemon thread if GUI mode
    isDaemon = True if guibool else False
    # Launch thread for MQTT
    mqttThread = threading.Thread(target=mqttSubStart,
                                args=(broIP,broPort,userName,userPwd,topics,guibool),
                                daemon=isDaemon)
    mqttThread.start()