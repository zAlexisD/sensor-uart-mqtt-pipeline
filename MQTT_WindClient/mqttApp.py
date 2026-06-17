"""
MQTT Application script - MQTT subscriber client in Windows
"""
from mqtt.manager import *
from mqtt.handlers import checkArgs,TopicSelectController

import sys
from PyQt6.QtWidgets import QApplication
from gui.mainWindow import MainWindow
from getpass import getpass

#TODO: Might add maximum listening time and/or max amount of data to store

def main(broIP:str,broPort:int,userName:str,userPwd:str,guiBool:bool=False):
    #TODO: Topic selection would be done here
    controller = TopicSelectController()
    # Connect Qt signal for topic list selection
    controller.topic_selection.connect(
        lambda topics: startMqttThread(topics,broIP,broPort,userName,userPwd,guiBool))

    if guiBool:
        # GUI Mode
        app = QApplication(sys.argv)
        window = MainWindow(controller,logs=True)
        window.show()
        sys.exit(app.exec())

    else:
        # CLI mode 
        controller.set_topics_from_cli()
        # Topic Selection -> Signal emitted → MQTT thread starts -> Launch MQTT Client

#TODO: GUI: Handle to subscribe/unsuscribe on the client ?

if __name__ == "__main__":
    args = checkArgs()
    # Check if user asks for private password typing
    if args.ask_pwd:
        args.pwd = getpass("Password: ")
    # Launch MQTT client
    main(args.ip,args.port,args.user,args.pwd,args.gui)

    # # Debug GUI
    # controller = TopicSelectController()
    # app = QApplication(sys.argv)
    # window = MainWindow(controller,True)
    # window.show()
    # sys.exit(app.exec())