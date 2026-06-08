# MQTT Application

In the context of an internship small project, this repostitory presents an end-to-end IoT pipeline using NXP SDKs to interface Murata UWB chips via UART with Raspberry Pi MQTT broker, streaming real-time data to a Windows client.

## Requirements

### Hardware Requirements

| **Component** | **Description** | **Purpose in Pipeline** |
|--------------|-----------------|--------------------------|
| **[MQTT‑capable server](ca://s?q=Explain_MQTT_broker_server_requirement)** | Any machine capable of running an MQTT broker (Raspberry Pi, Linux server, Windows machine, cloud VM). | Hosts the Mosquitto broker and acts as the central message hub. |
| **[Raspberry Pi](ca://s?q=Explain_Raspberry_Pi_role)** (or equivalent SBC) | Used as the UART data receiver and MQTT publisher. Must expose a serial port (`/dev/serial0`). | Bridges UART sensor data → MQTT topics. |
| **[UART‑enabled sensor](ca://s?q=Explain_UART_sensor_requirement)** | Any sensor capable of sending data over UART. In our case: **Murata Type 2BP**. | Provides real‑time measurement data to the Raspberry Pi. |
| **[USB‑UART cable](ca://s?q=Explain_UART_cable_requirement)** | For debugging or connecting the sensor to other hosts if needed. | Optional but useful for development and testing. |
| **[Windows PC](ca://s?q=Explain_Windows_PC_role)** | Runs the MQTT subscriber application. | Displays or processes the data published by the Pi. |

---

### Software Requirements

| **Software** | **Description** | **Installation / Link** |
|--------------|-----------------|--------------------------|
| **[Python 3.10+](ca://s?q=Explain_Python_requirement)** | Required for the Raspberry Pi publisher and Windows subscriber scripts. | https://www.python.org/downloads/ |
| **[Python libraries](ca://s?q=Explain_Python_libraries_requirement)** | `paho-mqtt`, `pyserial`, `numpy`, etc. Listed in `requirements.txt`. | `pip install -r requirements.txt` |
| **[Mosquitto MQTT Broker](ca://s?q=Explain_Mosquitto_requirement)** | Lightweight MQTT broker running on the Raspberry Pi or remote server. | https://mosquitto.org/download/ |
| **[MQTT Explorer](ca://s?q=Explain_MQTT_Explorer_requirement)** (optional) | GUI tool for inspecting topics and debugging MQTT traffic. | https://mqtt-explorer.com/ |
| **[NXP MCUXpresso IDE](ca://s?q=Explain_MCUXpresso_requirement)** | Required only if you need to reprogram or debug the Murata Type 2BP firmware. | https://www.nxp.com/mcuxpresso |

## Project Folder Structure

| **Folder** | **Description** | **Role in Pipeline** |
|-----------|-----------------|-----------------------|
| **[MQTT_WindClient](ca://s?q=Explain_Windows_MQTT_client_folder)** | Contains the Windows‑side MQTT subscriber and GUI application. Includes MQTT client logic, callbacks, and visualization scripts. | Subscribes to MQTT topics and displays or processes incoming sensor data. |
| **[MQTT_RaspClient](ca://s?q=Explain_Raspberry_MQTT_client_folder)** | Contains the Raspberry Pi publisher logic, including UART reading, frame parsing, and MQTT publishing. | Reads UART data from the sensor and publishes structured messages to the MQTT broker. |

The project is divided into two main components: the **Raspberry Pi publisher**, responsible for acquiring UART data from the Murata Type 2BP sensor and publishing it to the MQTT broker, and the **Windows client subscriber**, which receives, visualizes, and processes the published data. This separation ensures a clean architecture where data acquisition and data consumption remain independent and modular.

Additionaly:
- `livePlot.py` is a sample test script for live scrolling plots with multi widgets for values such as **Temperature** and **Battery Level**.
- `serialListening.py` is the test script for continuously read and display incoming serial data on a specific port -> usage: ``` python3 serialListening.py <COM_Port> ```
- `simpleGUI.py` is a sample test script to display serial data on a GUI within various widgets

## Usage

The following steps describe how to deploy and run the complete MQTT data pipeline across the Raspberry Pi (publisher), the MQTT broker, and the Windows client (subscriber).

### 1. Clone the Repository

- Clone repository
  ```bash
  git clone <https://github.com/zAlexisD/MQTT_App>```
- Place the `MQTT_RaspClient` folder on the Raspberry Pi workspace.
- Place the `MQTT_WindClient` folder on the Windows machine.

### 2. Prepare the Raspberry Pi (Publisher)

- **[Connect UART sensor](#sensor-side)**
- **[Configure MQTT Broker](#raspberry-pi-broker)**
- **Run the Raspberry Pi publisher**
```bash
python3 mqttApp.py
```

### 3. Prepare the Windows Client (Subscriber)

- **[Configure broker address and connection settings](#windows-client)**
- **Run the Windows subscriber**
```bash
python3 mqttApp.py <gui_bool>
```

 Where:
- `True` → Launches the GUI
- `False` → Runs subscriber logic without GUI

## Sensor Side

This section describes the firmware running on the Murata Type 2BP sensor, the flashing procedure, and the UART data format used by the MQTT pipeline.

---

### 1. Firmware Origin and Licensing

- **[NXP SDK base](ca://s?q=Explain_NXP_SDK_origin)**  
  The firmware running on the Murata Type 2BP is originally derived from NXP’s official SDK sample projects.

- **[Murata restricted code](ca://s?q=Explain_Murata_restricted_code_warning)**  
  Some components of the original firmware are part of Murata’s restricted software package and cannot be redistributed.

As a result, only **customized source files** developed for this project are shared publicly.

---

### 2. Custom Firmware Repository

The modified source files used to adapt the Murata Type 2BP behavior (UART output, frame formatting, etc.) are available in the following repository:

  **➡️ <.../CustomedApp_NXPqn9090>**

This repository contains only the **custom code**, not the full SDK.

**Note:** In this repository, only the case `#if defined(CUSTOM_...)` interests us (i.e the folders ...).

---

### 3. Flashing the Firmware (DK6Programmer)

To flash the compiled binary (`.bin`) into the Murata Type 2BP, use **DK6Programmer** (provided in the NXP SDK), the official flashing tool for DK6‑family MCUs.

- **DK6Programmer usage**  
  In the folder where the `DK6Programmer.exe` is located and run:

```bash
.\DK6Programmer.exe -V 0 -P 1000000 -s <chip_COM_port> -Y -p <fileName.bin> 
```

- `<chip_COM_port>` the serial port on which the chip is connected
- `<fileName.bin>` path to the compiled binary

You can then test with `serialListening.py` to look at the chip's output

**Note:** Make sure that your binary file makes your chip working in **Standalone mode**.

---

### 4. UART Data format

The Murata Type 2BP sends measurement data over UART using a structured ASCII format.

For simplicity, we put the measured data inside the chip's logs and structured into 3 datatypes `CONFIG`,`STATUS` and `INFO`. They are then presented in the following format:
```
[CONFIG]: INFO: "DeviceInfo": "Device Name": "UWB-IoT-2BP"
[STATUS]: INFO: "UWBSessionstate": 0
[INFO]: INFO: "ADCTemperature": 40°C
...
```

The common `INFO` corresponds to the priority level of the log.

## Raspberry Pi Broker

This section describes how the Raspberry Pi is configured to act as the MQTT broker using Mosquitto, including user authentication, port configuration, and basic publisher/subscriber commands for testing.

---

### 1. Install and Configure Mosquitto

- **Install Mosquitto**  
```bash
  sudo apt update
  sudo apt install mosquitto mosquitto-clients
  sudo systemctl enable mosquitto
```
- Verify broker status
```bash
systemctl status mosquitto
```

---

### 2. Configure Authentification (User/Password)

- **Create Mosquitto password file**
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd <username>
```
- **Update Mosquitto configuration**

Edit `/etc/mosquitto/mosquitto.conf` and add:
```
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883
```
- **Restart broker**
```bash
sudo systemctl restart mosquitto
```

---

### 3. Test the broker (Publisher/Subscriber Commands)

These commands help validate that the broker is running correctly before integrating the Raspberry Pi publisher and Windows subscriber.

- **Test subscriber**
```bash
mosquitto_sub -h localhost -t "test/topic" -u <username> -P <password>
```
- **Test publisher**
```bash
mosquitto_pub -h localhost -t "test/topic" -m "hello world" -u <username> -P <password>
```

If the subscriber receives `hello world`, the broker is correctly configured.

---

### 4. Network and Port Considerations

- **Default MQTT port:** `1883`
- Ensure the Raspberry Pi and Windows client are on the same network.
- If using firewalls or routers, ensure port `1883` is open.
- If using a remote server instead of a Pi, update the Windows client configuration accordingly.

## Raspberry Pi

The Raspberry Pi acts as the **data acquisition and publishing node** in the MQTT pipeline.  
It listens to the sensor’s UART output, extracts relevant measurement fields, converts them into structured key–value pairs, and publishes them to the MQTT broker under well‑defined topic names.

---

### 1. Serial Port Listening

- **[Open UART interface](ca://s?q=Explain_RPi_UART_opening)**  
  The Raspberry Pi listens on `/dev/serial0` (or another configured UART port).  
  The script continuously reads incoming lines from the Murata Type 2BP sensor.

- **[Raw data ingestion](ca://s?q=Explain_RPi_raw_data_ingestion)**  
  The sensor outputs mixed logs (debug, status, measurement frames).  
  The Pi captures all incoming lines before filtering.

---

### 2. Log Filtering and Data Extraction

- **[Filter relevant frames](ca://s?q=Explain_RPi_filtering_logic)**  
  Only lines containing chosen fields (`[CONFIG]`, `[STATUS]`, `[INFO]`) are kept.  
  All other logs are ignored to avoid polluting MQTT topics.

- **[Parse key/value pairs](ca://s?q=Explain_RPi_parsing_logic)**  
  Each valid line is split into:
  - **Datatype** → becomes the MQTT topic name  
  - **Value** → becomes the MQTT message payload  

  Example:
  ```
  [INFO]: INFO: "ADCTemperature": 40°C
  ```
  Becomes:
  - Topic → `"ADCTemperature"`
  - Payload → `40°C`

---

### 3. Publishing to MQTT Broker

- **MQTT client setup**
The Raspberry Pi uses the Paho MQTT client to connect to the broker (local or remote).
- **Publish loop**
For each parsed measurement:
```bash
client.publish(topic, value)
```
- **Error Handling**
The scripts includes:
    - reconnection logic
    - serial read timeouts
    - malformed frame detection

## Windows Client

The Windows client acts as the **MQTT subscriber and data visualization node**.  
It connects to the broker, listens for incoming sensor topics, stores the received values in structured JSON files, and optionally forwards the data to a GUI when enabled.

---

### 1. MQTT Connection and Subscription

- **[Connect to broker](ca://s?q=Explain_Windows_client_connect_broker)**  
  The client initializes a Paho MQTT instance and connects to the broker using the configured IP address and port.

- **[Subscribe to topics](ca://s?q=Explain_Windows_client_subscribe_topics)**  
  The client subscribes to all relevant sensor topics (e.g., `"ADCTemperature"`) and enters a continuous listening loop.

- **[Listening mode](ca://s?q=Explain_Windows_client_listening_mode)**  
  Once connected, the client waits for incoming messages and triggers the `on_message` callback whenever new data arrives.

---

### 2. Message Handling and Data Conversion

- **[Convert MQTT payload to dictionary](ca://s?q=Explain_Windows_client_payload_conversion)**  
  Each received message is parsed into a Python dictionary and handled differently based on field:
    - CONFIG:
    ```python
    {
        "DeviceInfo": {
            "DeviceName": "name",
            "DeviceMACaddr": "MAC",
            ...},
        "RangingParams": {
            "DevMacAddr": "DeviceMAC",
            "DestMacAddr": "DestinationMAC",
            ...}
    }
    ```
    - STATUS:
    ```python
    {
        "UwbSessionState": state,
        "phHbci": state,
        ...
    }
    ```
    - INFO:
    ```python
    {
        "ADCTemperature":[
            {
                "Message Count": 1,
                "Value": 26,
                "Timestamp": 20260505185045
            },
            {
                "Message Count": 2,
                "Value": 27,
                "Timestamp": 20260505185050
            }
        ],
        "BatteryLevel":[
            {
                "Message Count": 1,
                "Value": 100,
                "Timestamp": 20260505185045
            },
            {
                "Message Count": 2,
                "Value": 99,
                "Timestamp": 20260505185050
            }
        ]
    }
    ```
- **Topic-based routing**
The topic name determines which JSON file must be updated.
    - Configuration data is updated once in the config file
    - Status and Info are in the same file but only Info data is updated at each timestamp

---

### 3. JSON File Storage

- **Update JSON files**

    For each message:
    - Load the existing JSON file (or create it if missing)
    - Insert or update the new value
    - Save the file back to disk

    This ensures persistent, structured storage of all incoming sensor data.

- **File organization**  
JSON files are grouped by measurement type, making them easy to inspect or process later.

---

### 4. GUI Integration (Optional)

- **GUI activation flag**
    
    The Client is lauch with:
    ```bash
    python3 mqttApp.py <gui_bool>
    ```
    - `True` → GUI enabled
    - `False` → console‑only mode

- **Forward data to GUI**  
When GUI mode is active, each parsed dictionary is forwarded to the GUI update function, enabling real‑time visualization.

- **Decoupled architecture**  
The GUI never interacts directly with MQTT; it only receives processed data from the subscriber logic.

## Results


## Future improvements