"""
MQTT Application script - MQTT subscriber client in Windows
"""
from mqtt.manager import *
from mqtt.config import topicList,brokerIP,brokerPort,clientUsername,clientPwd
from mqtt.layout import CONSOLE_HEADER
import argparse
import sys
import threading
from PyQt6.QtWidgets import QApplication
from gui.mainWindow import MainWindow
from getpass import getpass

#TODO: Add user data selection choice (buttons? for GUI), (option1, option2, ..., various ones, all)
#TODO: Might add maximum listening time and/or max amount of data to store

def mqttSubStart(broIP,broPort,userName,userPwd,topics:list[str]=topicList):
    print(CONSOLE_HEADER)
    # MQTT Subscriber Client loop
    mqttc = newClient(brokIP=broIP,brokPort=broPort,cliUser=userName,cliPwd=userPwd)
    #TODO: Topic selection would be done here
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
        
def checkArgs():
    parser = argparse.ArgumentParser(description="MQTT Client")

    # GUI Flag -> set to True if --gui is passed
    parser.add_argument("--gui",action="store_true",help="Enable GUI Mode")

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
    parser.add_argument("--ask-pwd", action="store_true",
                    help="Prompt for password securely")
    
    return parser.parse_args()

def main(broIP:str,broPort:int,userName:str,userPwd:str,guiBool:bool=False):
    if guiBool:
        # Launch thread for MQTT
        mqttThread = threading.Thread(target=mqttSubStart,
                                      args=(broIP,broPort,userName,userPwd),
                                      daemon=True)
        mqttThread.start()
        # Launch GUI in main thread
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    else:
        mqttSubStart(broIP,broPort,userName,userPwd)

#TODO: GUI: Open window, ask for user to start the MQTT subscription to launch and get data -> does it need a specific thread ?

if __name__ == "__main__":
    args = checkArgs()
    # Check if user asks for private password typing
    if args.ask_password:
        args.pwd = getpass("Password: ")
    # Launch MQTT client
    main(args.ip,args.port,args.user,args.pwd,args.gui)