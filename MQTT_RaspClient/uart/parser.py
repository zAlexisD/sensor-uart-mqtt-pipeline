"""
Parser class converts UART into structured data
"""

class UARTParser:
    def parse(self, line):
        """
        Converts a UART line into a dict.
        Example input:
            "RANGE=2.34;BATT=3.01;STATUS=OK"
        Output:
            {"range": 2.34, "battery": 3.01, "status": "OK"}
        """
        if line is None:
            print("No Line")
            return None

        tagData = {}
        try:
            if ": " in line:
                # Handle [CONFIG] data type
                if line.startswith("[CONFIG]"):
                    # type-> [CONFIG]:INFO  : Device Info: Device Name: SR150_PROD_IOT_ROW
                    _,configtype,key,value = line.split(": ")
                    try:
                        # Topics don't handle spaces
                        configtype.replace(" ","")
                        key.replace(" ","")
                        value = str(value)
                    except ValueError:
                        pass
                    tagData[configtype][key] = value

                # Handle [INFO] data type
                if line.startswith("[INFO]"):
                    # type-> [INFO] :INFO : Timestamp: 746373863
                    _,key,value = line.split(": ")
                    # Special case for temperature
                    #TODO: might make binary file only return numerical value for temp
                    if key == "ADC Temperature":
                        value,_ = value.split("°")
                    try:
                        key.replace(" ","")
                        value = int(value)
                    except ValueError:
                        pass
                    tagData[key] = value

                # Handle Status data type
                #TODO: actually phHbci always return False so we might ignore that case
                if line.startswith("[STATUS]"):
                    key,value = line.split(": ")
                    try:
                        key.replace(" ","")
                        value = str(value)
                    except ValueError:
                        pass
                    tagData[key] = value

            return tagData if tagData else None

        except Exception as e:
            print(f"[PARSER] Error parsing line '{line}': {e}")
            return None