"""
MQTT Application script - MQTT subscriber client in Windows
"""
from mqtt.manager import *
from mqtt.handlers import checkArgs,TopicSelectController,startMqttThread
import sys
from PyQt6.QtWidgets import QApplication
from gui.mainWindow import MainWindow
from getpass import getpass

#TODO: Add user data selection choice (buttons? for GUI), (option1, option2, ..., various ones, all)
#TODO: Might add maximum listening time and/or max amount of data to store

def main(broIP:str,broPort:int,userName:str,userPwd:str,guiBool:bool=False):
    #TODO: Topic selection would be done here
    controller = TopicSelectController()
    # Connect Qt signal for topic list selection
    controller.topic_selection.connect(
        lambda topics: startMqttThread(topics,broIP,broPort,userName,userPwd))

    if guiBool:
        # GUI Mode
        app = QApplication(sys.argv)
        window = MainWindow(controller)
        window.show()
        sys.exit(app.exec())

    else:
         # CLI mode
        controller.set_topics_from_cli()
        # Signal emitted → MQTT thread starts

#TODO: GUI: Open window, ask for user to start the MQTT subscription to launch and get data -> does it need a specific thread ?

if __name__ == "__main__":
    # args = checkArgs()
    # # Check if user asks for private password typing
    # if args.ask_password:
    #     args.pwd = getpass("Password: ")
    # # Launch MQTT client
    # main(args.ip,args.port,args.user,args.pwd,args.gui)

    # Debug GUI
    controller = TopicSelectController()
    app = QApplication(sys.argv)
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec())