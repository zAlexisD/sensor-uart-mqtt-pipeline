import serial
import time
from settings import tagCOM,tagBaud

#TODO: handle message content to only send relevant data -> might manage that in tag binary

class UARTReader:
    def __init__(self, port=tagCOM, baudrate=tagBaud, timeout=0.05):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
            print(f"Listening on {port} at {baudrate} baud...")
        except serial.SerialException as e:
            print(f"Failed to open port {port}: {e}")

    def read_line(self):
        """
        Reads one line from UART (ASCII-based protocol).
        Returns None if nothing received.
        """
        try:
            if self.ser.in_waiting > 0:  # Check if data is available
                line = self.ser.readline().decode(errors='replace').strip()
                if line:
                    return line
            else:
                time.sleep(0.05)  # Avoid busy-waiting
        except UnicodeDecodeError:
            print("Warning: Received non-text data.")
            return None
        except serial.SerialException as e:
            print(f"[UART] Error: {e}")
            return None