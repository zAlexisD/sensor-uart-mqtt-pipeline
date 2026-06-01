# MQTT Application

In the context of an internship small project, this repostitory presents an end-to-end IoT pipeline using NXP SDKs to interface Murata UWB chips via UART with Raspberry Pi MQTT broker, streaming real-time data to a Windows client.

## Requirements



## Usage



## Sensor side : 

warn: the building project samples are extract from NXP SDKs

see repository .../CustomedApp_NXPqn9090

## Raspberry Pi Broker



## Raspberry Pi 



## Windows Client



## Results



## Appendix

- `livePlot.py` is a sample test script for live scrolling plots with multi widgets for values such as **Temperature** and **Battery Level**.
- `serialListening.py` is the test script for continuously read and display incoming serial data on a specific port -> usage: ``` python3 serialListening.py <COM_Port> ```
- `simpleGUI.py` is a sample test script to display serial data on a GUI within various widgets