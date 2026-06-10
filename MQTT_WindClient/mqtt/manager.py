"""
MQTT Module for helpers definition
"""
import paho.mqtt.client as mqtt
from utils.config import *
from mqtt.callbacks import *
from mqtt.layout import dispStatus,COMMANDS_HEADER,CONSOLE_HEADER

def newClient(logs:bool = False,
              brokIP:str = brokerIP,brokPort:int = brokerPort,
              cliUser:str = clientUsername,cliPwd:str = clientPwd) -> mqtt:
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,client_id=clientID)
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

def loopSession(client: mqtt, topic: list = wholeList):
    # Add 1st loop flag for correct print ordering and launching listening loop
    firstLoop = True
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

def mqttSubStart(broIP,broPort,userName,userPwd,topics:list[str]=topicList):
    print(CONSOLE_HEADER)
    # MQTT Subscriber Client loop
    mqttc = newClient(brokIP=broIP,brokPort=broPort,cliUser=userName,cliPwd=userPwd)
    reqSubscription(mqttc,topics)

    try:
        loopSession(mqttc,topics)
    except KeyboardInterrupt:
        # CTRL + C
        print("Stopped by user, disconnecting...")
        reqDisconnect(mqttc)
        print("MQTT connection closed")
    except Exception as e:
        print(f"Error: {e}")