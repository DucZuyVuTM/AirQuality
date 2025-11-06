"""
Air Quality Emulator for Rightech IoT Cloud (RIC)
Publishes random data to RIC via MQTT - UPDATED VERSION
"""

import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime

class AirQualityEmulatorRIC:
    def __init__(self, device_id="mqtt-duczuyvu12-9qx79c",
                 broker="dev.rightech.io", port=1883,
                 username="livingroom-username",
                 password="living",
                 object_id="69032e296dffe6c39bbb2cd0"):
        
        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.object_id = object_id
        
        # Dựa trên state data từ API response, có vẻ Rightech dùng topic dạng "base/state/<sensor>"
        self.topic_base = "base/state"
        
        # Tạo MQTT client với client_id duy nhất
        self.client = mqtt.Client(client_id=f"emulator_{device_id}", protocol=mqtt.MQTTv311)
        self.client.username_pw_set(username, password)
        self.interval = 30

        # Kết nối tới Rightech
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            print(f"✅ Kết nối thành công tới Rightech IoT Cloud: {self.broker}:{self.port}")
            print(f"📡 Device ID: {self.device_id}")
            print(f"📦 Object ID: {self.object_id}")
            print(f"📊 Topic base: {self.topic_base}/<sensor>")
        except Exception as e:
            print(f"❌ Lỗi kết nối tới Rightech: {e}")
            exit(1)

    def generate_sensor_data(self):
        """Tạo dữ liệu cảm biến ngẫu nhiên với logic thực tế"""
        # PM2.5: 5-100 µg/m³, thường 15-35, nguy hiểm >35
        pm25 = max(5, min(100, random.gauss(25, 10)))
        
        # PM10: thường cao hơn PM2.5 10-30 µg/m³
        pm10 = max(10, pm25 + random.uniform(5, 25))
        
        # CO2: 400-2000 ppm, thường 400-800, nguy hiểm >1000
        co2 = max(400, min(2000, random.gauss(600, 150)))
        
        # Nhiệt độ: 18-32°C, comfort: 22-26°C
        temperature = max(18, min(32, random.gauss(24, 3)))
        
        # Độ ẩm: 30-80%, comfort: 40-60%
        humidity = max(30, min(80, random.gauss(50, 10)))
        
        # Logic điều khiển relay (máy lọc không khí)
        relay_state = pm25 > 35 or pm10 > 50 or co2 > 1000
        
        # Trạng thái cảnh báo
        if pm25 > 35 or pm10 > 50 or co2 > 1000:
            status = "DANGER"
        elif pm25 > 25 or pm10 > 35 or co2 > 800:
            status = "WARNING"
        else:
            status = "GOOD"

        return {
            "pm25": round(pm25, 1),
            "pm10": round(pm10, 1),
            "co2": int(co2),
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "relay_state": 1 if relay_state else 0,
            "status": status,
            "online": True,  # Quan trọng: thiết bị online
            "timestamp": int(time.time() * 1000)  # Rightech dùng timestamp milliseconds
        }

    def display_and_publish(self, data):
        """Hiển thị và gửi dữ liệu lên RIC"""
        print(f"\n{'='*60}")
        print(f"🌫️ AIR QUALITY DATA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"📟 Device:      {self.device_id}")
        print(f"🔴 PM2.5:       {data['pm25']} µg/m³ {'🚨 Warning' if data['pm25'] > 35 else ''}")
        print(f"🟠 PM10:        {data['pm10']} µg/m³ {'🚨 Warning' if data['pm10'] > 50 else ''}")
        print(f"💨 CO2:         {data['co2']} ppm {'🚨 Warning' if data['co2'] > 1000 else ''}")
        print(f"🌡️  Temp:        {data['temperature']}°C")
        print(f"💧 Humidity:    {data['humidity']}%")
        print(f"🔌 Relay:       {'🔴 ON' if data['relay_state'] else '🟢 OFF'}")
        print(f"📊 Status:      {data['status']}")
        print(f"🟢 Online:      {data['online']}")

        try:
            # Gửi từng giá trị sensor theo topic structure từ API response
            self.client.publish(f"{self.topic_base}/pm25", data['pm25'], qos=1)
            self.client.publish(f"{self.topic_base}/pm10", data['pm10'], qos=1)
            self.client.publish(f"{self.topic_base}/co2", data['co2'], qos=1)
            self.client.publish(f"{self.topic_base}/temperature", data['temperature'], qos=1)
            self.client.publish(f"{self.topic_base}/humidity", data['humidity'], qos=1)
            self.client.publish(f"{self.topic_base}/relay_state", data['relay_state'], qos=1)
            self.client.publish(f"{self.topic_base}/status", data['status'], qos=1)
            self.client.publish(f"{self.topic_base}/online", data['online'], qos=1)
            
            # Có thể publish cả object state nếu cần
            state_data = {
                "temperature": data['temperature'],
                "humidity": data['humidity'],
                "pm25": data['pm25'],
                "pm10": data['pm10'],
                "co2": data['co2'],
                "online": data['online'],
                "timestamp": data['timestamp']
            }
            
            print(f"✅ Gửi thành công {len(state_data)} sensors lên Rightech")
            print(f"📡 Topic pattern: {self.topic_base}/<sensor_name>")
            
        except Exception as e:
            print(f"❌ Lỗi gửi dữ liệu: {e}")

        print(f"{'='*60}")

    def run(self):
        """Chạy emulator"""
        max_cycles = 3

        print(f"\n🚀 BẮT ĐẦU GỬI DỮ LIỆU LÊN RIGHTECH IOT CLOUD")
        print(f"⏰ Interval: {self.interval}s | Số chu kỳ: {max_cycles}")
        print(f"🔧 Broker: {self.broker}:{self.port}")
        
        cycle = 0        
        
        try:
            while cycle < max_cycles:
                cycle += 1
                print(f"\n📦 Chu kỳ #{cycle}/{max_cycles}")
                
                # Mô phỏng thời gian đọc cảm biến
                time.sleep(random.uniform(1.0, 2.0))
                
                # Tạo và gửi dữ liệu
                data = self.generate_sensor_data()
                self.display_and_publish(data)
                
                # Chờ giữa các chu kỳ (trừ chu kỳ cuối)
                if cycle < max_cycles:
                    print(f"⏳ Chờ {self.interval}s đến chu kỳ tiếp theo...")
                    time.sleep(self.interval)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Dừng bởi người dùng.")
        finally:
            # Gửi trạng thái offline trước khi disconnect
            try:
                offline_data = {"online": False, "timestamp": int(time.time() * 1000)}
                self.client.publish(f"{self.topic_base}/online", False, qos=1)
                print("📴 Đã gửi trạng thái offline")
            except:
                pass
                
            self.client.disconnect()
            print("🔌 Đã ngắt kết nối khỏi Rightech IoT Cloud.")

# === MAIN ===
if __name__ == "__main__":
    print("🌐 Air Quality Emulator for Rightech IoT Cloud")
    print("=" * 50)
    
    # Sử dụng thông tin chính xác từ API response
    emulator = AirQualityEmulatorRIC(
        device_id="mqtt-duczuyvu12-9qx79c",      # Khớp với field "id" trong API
        username="livingroom-username",          # Giữ nguyên
        password="living",                       # Giữ nguyên  
        object_id="69032e296dffe6c39bbb2cd0"    # Object ID thực từ API _id field
    )
    emulator.run()
