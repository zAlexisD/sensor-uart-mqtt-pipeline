"""
Parser class converts UART into structured data
"""
import re

class UARTParser:
    def __init__(self):
        pass
    
    #TODO: Now good to adapt for our customed 2BP but might handle for any sensor later
    def parse(self, line:str):
        """
        Converts a UART line into a dictionary
        Example input:
            [INFO]  :INFO : ADC Temperature: 40°C
            [STATUS]:INFO : phHbci: FAILURE
        Output:
            {"ADCTemperature": 40}
            {"phHbciStatus": "FAILURE"}
        """

        # First make sure the line is not encoded differently or have hidden codes
        line = self.remove_ansi(line)

        if not line:
            print("No Line")
            return None

        tagData = {}
        try:
            # First remove all spaces for efficiency and as topic do not handle them
            handledLine = "".join(line.split())

            if ":" in handledLine:
                # Handle [CONFIG] data type -> {ConfigType:{ConfigKey:Value}}
                if handledLine.startswith("[CONFIG]"):
                    # type-> [CONFIG]:INFO:DeviceInfo:DeviceName:SR150_PROD_IOT_ROW
                    _,_,configtype,key,value = handledLine.split(":")
                    try:
                        value = str(value)
                    except ValueError:
                        pass
                    tagData[configtype][key] = value

                # Handle [INFO] data type -> {InfoType:Value}
                if handledLine.startswith("[INFO]"):
                    # type-> [INFO]:INFO:Timestamp:746373863
                    _,_,key,value = handledLine.split(":")
                    # If temperature, remove the unit to keep only numbers
                    #TODO: might make binary file only return numerical value for temp
                    if key == "ADCTemperature":
                        value,_ = value.split("°")
                    try:
                        #TODO: might consider float instead of int for more general cases
                        value = int(value)
                    except ValueError:
                        pass
                    tagData[key] = value

                # Handle [Status] data type -> {StatusType:Value}
                if handledLine.startswith("[STATUS]"):
                    # type-> [STATUS]:INFO:phHbci:FAILURE
                    _,_,key,value = handledLine.split(":")
                    try:
                        value = str(value)
                    except ValueError:
                        pass
                    tagData[key] = value

            return tagData if tagData else None

        except Exception as e:
            print(f"[PARSER] Error parsing line '{handledLine}': {e}")
            return None
        
    def remove_ansi(self, text):
        ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ANSI_ESCAPE.sub('',text)