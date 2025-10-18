"""
IoT Air Quality Monitor Emulator
Simulates ESP32 + SDS011, MH-Z19B, DHT22, Relay Module
Publishes random data to MQTT broker
"""

import json
import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime

class AirQualityEmulator:
    def __init__(self, device_id="air_monitor_001", broker="localhost", port=1883):
        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id=f"emulator_{device_id}", protocol=mqtt.MQTTv311)
        self.running = False
        self.interval = 30  # Seconds between readings

        # Connect to MQTT broker
        try:
            self.client.connect(self.broker, self.port, 60)
            print(f"Connected to MQTT broker at {self.broker}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            exit(1)

    def generate_sensor_data(self):
        """Generate simulated sensor data"""
        pm25_trend = random.uniform(-2, 2)
        pm25 = max(5, min(100, 25 + pm25_trend + random.uniform(-5, 5)))
        pm10 = pm25 + random.uniform(10, 20)
        co2_base = 450 if random.random() > 0.7 else 800
        co2 = max(400, min(2000, co2_base + random.uniform(-50, 100)))
        temperature = max(18, min(28, 22 + random.uniform(-2, 2)))
        humidity = max(30, min(70, 50 + random.uniform(-10, 10)))
        relay_state = pm25 > 50 and random.random() > 0.3

        return {
            "device_id": self.device_id,
            "timestamp": int(time.time()),
            "datetime": datetime.now().isoformat(),
            "pm25": round(pm25, 1),
            "pm10": round(pm10, 1),
            "co2": int(co2),
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "relay_state": relay_state,
            "status": "OK" if pm25 < 100 else "WARNING"
        }

    def display_data(self, data):
        """Display data in console and publish to MQTT"""
        print(f"\n{'='*60}")
        print(f"📊 AIR QUALITY DATA - {data['datetime']}")
        print(f"{'='*60}")
        print(f"🆔 Device:      {data['device_id']}")
        print(f"⏰ Time:        {datetime.fromtimestamp(data['timestamp']).strftime('%H:%M:%S')}")
        print(f"🌫️ PM2.5:       {data['pm25']} µg/m³ {'⚠️' if data['pm25'] > 35 else ''}")
        print(f"💨 PM10:        {data['pm10']} µg/m³")
        print(f"🌡️ CO2:         {data['co2']} ppm {'⚠️' if data['co2'] > 1000 else ''}")
        print(f"🌡️ Temperature: {data['temperature']}°C")
        print(f"💧 Humidity:    {data['humidity']}%")
        print(f"🔌 Relay:       {'🟢 ON' if data['relay_state'] else '🔴 OFF'}")
        print(f"📈 Status:      {data['status']}")

        # Publish to MQTT topics
        self.client.publish("v1/devices/me/telemetry/pm25", data['pm25'], qos=1)
        self.client.publish("v1/devices/me/telemetry/pm10", data['pm10'], qos=1)
        self.client.publish("v1/devices/me/telemetry/co2", data['co2'], qos=1)
        self.client.publish("v1/devices/me/telemetry/temperature", data['temperature'], qos=1)
        self.client.publish("v1/devices/me/telemetry/humidity", data['humidity'], qos=1)
        self.client.publish("v1/devices/me/telemetry/relay_state", 1 if data['relay_state'] else 0, qos=1)
        status_json = json.dumps({"timestamp": data['timestamp'], "status": data['status']})
        self.client.publish("v1/devices/me/attributes", status_json, qos=1)
        print(f"📡 Published to MQTT topics")
        print(f"{'='*60}\n")

    def run_simulation(self):
        """Run simulation loop"""
        print(f"🚀 STARTING IoT DEVICE SIMULATION: {self.device_id}")
        print(f"⏱️ Data reading interval: {self.interval} seconds")
        
        self.running = True
        cycle = 0
        
        while self.running:
            cycle += 1
            print(f"\n🔄 Cycle #{cycle} - Reading sensor data...")
            read_time = random.uniform(0.5, 2.0)
            print(f"   ⏳ Reading sensors... ({read_time:.1f}s)")
            time.sleep(read_time)
            
            data = self.generate_sensor_data()
            self.display_data(data)
            
            process_time = random.uniform(0.2, 0.5)
            print(f"   ⚙️ Processing and sending data... ({process_time:.1f}s)")
            time.sleep(process_time)
            
            if cycle < 3:  # Run 3 demo cycles
                print(f"   ⏳ Waiting {self.interval} seconds for next cycle...")
                time.sleep(self.interval)
            else:
                time.sleep(self.interval)
                print("✅ Simulation demo completed!")
                break
        
        self.running = False
        self.client.disconnect()
    
    def stop(self):
        """Stop simulation"""
        self.running = False
        self.client.disconnect()
        print("\n🛑 STOPPING IoT DEVICE SIMULATION")

if __name__ == "__main__":
    try:
        emulator = AirQualityEmulator("air_monitor_001", "localhost", 1883)
        emulator.run_simulation()
    except KeyboardInterrupt:
        print("\n⚠️  User interrupted program (Ctrl+C)")
        emulator.stop()
    except Exception as e:
        print(f"\n❌ Error: {e}")
