"""
Layout Module for CLI
"""
import paho.mqtt as mqtt

CONSOLE_HEADER = """
================================================
            MQTT Subscriber Console             
================================================            
Commands:
  exit                Quit the program
  status              Check connection status
  sub <topic>         Subscribe to topic
  unsub <topic>       Unsubscribe from topic
  help                Display commands
  topics              List possible topics
------------------------------------------------
"""
COMMANDS_HEADER = """
------------------------------------------------
Commands:
  exit                Quit the program
  status              Check connection status
  sub <topic>         Subscribe to topic
  unsub <topic>       Unsubscribe from topic
  help                Display commands
  topics              List possible topics
------------------------------------------------
"""

def dispStatus(client: mqtt,topic: list):
    statusLayout = f"""
------------------------------------------------
Listening topics: {topic}
Connected: {client.is_connected()}
------------------------------------------------
"""
    print(statusLayout)