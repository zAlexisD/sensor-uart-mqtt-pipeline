import serial
import sys
import time

def listen_serial(port_name, baud_rate=9600, timeout=1):
    """Continuously read from the given serial port."""
    try:
        with serial.Serial(port=port_name, baudrate=baud_rate, timeout=timeout) as ser:
            print(f"Listening on {port_name} at {baud_rate} baud...")
            while True:
                try:
                    if ser.in_waiting > 0:  # Check if data is available
                        data = ser.readline().decode(errors='replace').strip()
                        if data:
                            print(f"Received: {data}")
                    else:
                        time.sleep(0.05)  # Avoid busy-waiting
                except UnicodeDecodeError:
                    print("Warning: Received non-text data.")
                except serial.SerialException as e:
                    print(f"Serial error: {e}")
                    break
    except serial.SerialException as e:
        print(f"Failed to open port {port_name}: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if (arg.startswith("COM")):
            port = arg
    listen_serial(port, baud_rate=3000000)
