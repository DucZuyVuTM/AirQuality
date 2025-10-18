"""
IoT Air Quality Monitor Emulator
Simulates ESP32 + SDS011, MH-Z19B, DHT22, Relay Module
Generates random data and outputs to console (or simulates MQTT)
"""

import json
import time
import random
import threading
from datetime import datetime

class AirQualityEmulator:
    def __init__(self, device_id="air_monitor_001"):
        self.device_id = device_id
        self.running = False
        self.interval = 30  # Seconds between data readings
        
    def generate_sensor_data(self):
        """Generate simulated sensor data"""
        # PM2.5: 0-100 (random with trend increase/decrease)
        pm25_trend = random.uniform(-2, 2)
        pm25 = max(5, min(100, 25 + pm25_trend + random.uniform(-5, 5)))
        
        # PM10: similar to PM2.5 but 10-20% higher
        pm10 = pm25 + random.uniform(10, 20)
        
        # CO2: 400-2000 ppm (increases with "more people")
        co2_base = 450 if random.random() > 0.7 else 800
        co2 = max(400, min(2000, co2_base + random.uniform(-50, 100)))
        
        # Temperature: 18-28°C
        temperature = max(18, min(28, 22 + random.uniform(-2, 2)))
        
        # Humidity: 30-70%
        humidity = max(30, min(70, 50 + random.uniform(-10, 10)))
        
        # Relay state: random or based on PM2.5 > 50
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
        """Display data in console with formatted output"""
        print(f"\n{'='*60}")
        print(f"📊 AIR QUALITY DATA - {data['datetime']}")
        print(f"{'='*60}")
        print(f"🆔 Device: {data['device_id']}")
        print(f"⏰ Time: {datetime.fromtimestamp(data['timestamp']).strftime('%H:%M:%S')}")
        print(f"🌫️  PM2.5: {data['pm25']} µg/m³ {'⚠️' if data['pm25'] > 35 else ''}")
        print(f"💨 PM10:  {data['pm10']} µg/m³")
        print(f"🌡️  CO2:   {data['co2']} ppm {'⚠️' if data['co2'] > 1000 else ''}")
        print(f"🌡️  Temperature: {data['temperature']}°C")
        print(f"💧 Humidity:   {data['humidity']}%")
        print(f"🔌 Relay:   {'🟢 ON' if data['relay_state'] else '🔴 OFF'}")
        print(f"📈 Status: {data['status']}")
        
        # Simulate MQTT sending
        mqtt_payload = json.dumps({
            "pm25": data['pm25'],
            "pm10": data['pm10'],
            "co2": data['co2'],
            "temperature": data['temperature'],
            "humidity": data['humidity'],
            "relay_state": data['relay_state']
        })
        print(f"📡 Sending MQTT payload: {len(mqtt_payload)} bytes")
        print(f"{'='*60}\n")
    
    def run_simulation(self):
        """Run simulation loop"""
        print(f"🚀 STARTING IoT DEVICE SIMULATION: {self.device_id}")
        print(f"⏱️  Data reading interval: {self.interval} seconds")
        print(f"📡 Simulated MQTT connection to ThingsBoard...")
        
        self.running = True
        cycle = 0
        
        while self.running:
            cycle += 1
            print(f"\n🔄 Cycle #{cycle} - Reading sensor data...")
            
            # Simulate sensor reading time (0.5-2 seconds)
            read_time = random.uniform(0.5, 2.0)
            print(f"   ⏳ Reading sensors... ({read_time:.1f}s)")
            time.sleep(read_time)
            
            # Generate and display data
            data = self.generate_sensor_data()
            self.display_data(data)
            
            # Simulate processing and sending data (0.2-0.5s)
            process_time = random.uniform(0.2, 0.5)
            print(f"   ⚙️  Processing and sending data... ({process_time:.1f}s)")
            time.sleep(process_time)
            
            if cycle < 3:  # Run 3 demo cycles
                print(f"   ⏳ Waiting {self.interval} seconds for next cycle...")
                time.sleep(self.interval)
            else:
                print("✅ Simulation demo completed!")
                break
        
        self.running = False
    
    def stop(self):
        """Stop simulation"""
        self.running = False
        print("\n🛑 STOPPING IoT DEVICE SIMULATION")

# Run simulation
if __name__ == "__main__":
    try:
        # Initialize and run emulator
        emulator = AirQualityEmulator("air_monitor_001")
        emulator.run_simulation()
        
    except KeyboardInterrupt:
        print("\n⚠️  User interrupted program (Ctrl+C)")
        emulator.stop()
    except Exception as e:
        print(f"\n❌ Error: {e}")
