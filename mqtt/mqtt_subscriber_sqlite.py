import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime

# Initialize SQLite database
conn = sqlite3.connect('air_quality.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS telemetry 
                 (topic TEXT, value TEXT, received_at TEXT)''')
conn.commit()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe("v1/devices/me/telemetry/#", qos=1)
    client.subscribe("v1/devices/me/attributes", qos=1)

def on_message(client, userdata, msg):
    topic = msg.topic
    value = msg.payload.decode()
    received_at = datetime.now().isoformat()
    
    # Store in database
    cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?)", 
                  (topic, value, received_at))
    conn.commit()
    print(f"Received: {topic} = {value} at {received_at}")

client = mqtt.Client(client_id="subscriber_001", protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
