import json
import time

# Запрос данных у пользователя
device_id = input("Введите ID устройства (например, air_monitor_001): ")
pm25 = float(input("Введите PM2.5 (мкг/м³, 0-999): "))
pm10 = float(input("Введите PM10 (мкг/м³, 0-999): "))
co2 = int(input("Введите CO2 (ppm, 0-5000): "))
temperature = float(input("Введите температуру (°C, -40...+80): "))
humidity = float(input("Введите влажность (%, 0-100): "))
relay_state = input("Состояние реле (true/false): ").lower() == "true"

# Формирование данных
data = {
    "device_id": device_id,
    "timestamp": int(time.time()),
    "pm25": pm25,
    "pm10": pm10,
    "co2": co2,
    "temperature": temperature,
    "humidity": humidity,
    "relay_state": relay_state
}

# Сохранение в JSON-файл
with open("air_quality_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("JSON-файл успешно создан: air_quality_data.json")
