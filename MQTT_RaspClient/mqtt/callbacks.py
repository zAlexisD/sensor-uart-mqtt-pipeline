"""
MQTT Module for callbacks
"""

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"ERR: Failed to connect: {reason_code}. Retry connection")
    else:
        print("\n[INFO] Connected to MQTT Broker!")

def on_publish(client,userdata,mid,reason_code, properties):
    if reason_code.is_failure:
        print(f"ERR: Failed to publish: {reason_code}")
    else:
        print(f"[INFO] Message {mid} published with success")

def on_log(client, userdata, level, buf):
    print("LOG:", buf)